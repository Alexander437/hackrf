import sys
sys.path.append('/usr/local/lib/python3.12/site-packages')

import SoapySDR
import numpy as np
from fastapi import HTTPException, status

from backend.sdr.fft import fft
from backend.settings import settings
from backend.schemas.sdr import SdrConfig
from backend.utils import run_in_executor
from backend.sdr.logger import set_python_log_handler


set_python_log_handler()


class SDR:
    """
    https://github.com/pothosware/SoapySDR/wiki/PythonSupport
    """

    def __init__(self, driver: str, version: str):
        self.sdr = None
        self.rxStream = None
        self.iq_buff = np.array([0] * 1024, np.complex64)

        try:
            self.config = SdrConfig.model_validate({
                'sample_rate_m': settings.INIT_SAMPLE_RATE_M,
                'center_freq_m': settings.INIT_CENTER_FREQ_M,
                'driver': driver,
                'version': version,
            })
        except IndexError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось найти подключенных устройств"
            )
        self.set_sdr_driver(self.config)

    def set_sdr_driver(self, config: SdrConfig):
        try:
            self.stop_streaming()
            self.sdr = SoapySDR.Device({'driver': config.driver})
            self.set_sample_rate(sample_rate_m=config.sample_rate_m)
            self.set_center_freq(center_freq_m=config.center_freq_m)
            self._start_streaming()
        except RuntimeError as ex:
            if str(ex).endswith('device matches'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ошибка при подключении {config.driver}"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(ex)
                )
        self.config = config

    def _start_streaming(self):
        if self.sdr is not None:
            self.rxStream = self.sdr.setupStream(SoapySDR.SOAPY_SDR_RX, SoapySDR.SOAPY_SDR_CF32)
            self.sdr.activateStream(self.rxStream)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Вызов start streaming до объявления SDR"
            )

    def stop_streaming(self):
        if self.sdr is not None and self.rxStream is not None:
            self.sdr.deactivateStream(self.rxStream)  # stop streaming
            self.sdr.closeStream(self.rxStream)

    def get_info(self):
        return {
            'antennas': self.sdr.listAntennas(SoapySDR.SOAPY_SDR_RX, 0),  # ('TX/RX',)
            'gains': self.sdr.listGains(SoapySDR.SOAPY_SDR_RX, 0),  # ('LNA', 'AMP', 'VGA')
            'freqs': self.sdr.getFrequencyRange(SoapySDR.SOAPY_SDR_RX, 0)  # (0, 7.25e+09,)
        }

    def read_samples(self) -> np.ndarray | None:
        sr = self.sdr.readStream(self.rxStream, [self.iq_buff], len(self.iq_buff))
        if sr.ret <= 0:
            return
        return self.iq_buff

    def set_sample_rate(self, sample_rate_m: float):
        self.sdr.setSampleRate(SoapySDR.SOAPY_SDR_RX, 0, sample_rate_m * 1e6)
        self.config.sample_rate_m = sample_rate_m

    def set_center_freq(self, center_freq_m: float):
        self.sdr.setFrequency(SoapySDR.SOAPY_SDR_RX, 0, center_freq_m * 1e6)
        self.config.center_freq_m = center_freq_m

    def get_psd(self) -> dict[str, list] | None:
        buff = self.read_samples()
        if buff is None:
            return

        p, freqs, t = fft(self.iq_buff, self.config.sample_rate_m, self.config.center_freq_m,
                          settings.INIT_NFFT, settings.INIT_DETREND_FUNC, settings.INIT_NOVERLAP)

        return {
            "psd": p.mean(axis=1).tolist(),
            "freqs": freqs.tolist()
        }

    async def aget_psd(self) -> dict[str, list] | None:
        buff = self.read_samples()
        if buff is None:
            return

        p, freqs, t = await run_in_executor(
            fft,
            self.iq_buff,
            self.config.sample_rate_m,
            self.config.center_freq_m,
            settings.INIT_NFFT,
            settings.INIT_DETREND_FUNC,
            settings.INIT_NOVERLAP
        )

        return {
            "psd": p.mean(axis=1).tolist(),
            "freqs": freqs.tolist()
        }


# singleton: https://www.devbookmarks.com/p/fastapi-knowledge-dependency-injection-singleton

sdr_registry = {
    f"{res['driver']}:{res['label']}": SDR(driver=res["driver"], version=res["version"])
    for res in SoapySDR.Device.enumerate()
}


def get_sdr(key: str | None = None) -> SDR:
    if key is None:
        return list(sdr_registry.values())[0]
    else:
        try:
            return sdr_registry[key]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="SDR по данному запросу не найден"
            )
