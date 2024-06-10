import threading
from abc import ABC, abstractmethod

import numpy as np

from src.fft import fft
from src.settings import settings

# plt.style.use('./mpl_styles/dark.mplstyle')
font = {'family': 'DejaVu Sans', 'weight': 500, 'size': 14}
SDR_REGISTRY = {}


def register_sdr(provider: str, cls) -> None:
    global SDR_REGISTRY
    if provider in SDR_REGISTRY:
        raise ValueError(
            f"Error while registering class {cls.__name__}, already taken by {SDR_REGISTRY[provider].__name__}"
        )
    SDR_REGISTRY[provider] = cls(
        sample_rate_m=settings.INIT_SAMPLE_RATE_M,
        center_freq_m=settings.INIT_CENTER_FREQ_M
    )


class SDR(ABC):

    @abstractmethod
    def read_samples(self) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def set_sample_rate(self, sample_rate: int):
        raise NotImplementedError

    @abstractmethod
    def set_center_freq(self, sample_rate: int):
        raise NotImplementedError

    def get_graphs(self, NFFT: int, detrend: str, noverlap: int):
        iq = self.read_samples()

        if iq is not None:
            self.ax1.clear()
            self.ax2.clear()
            P, freqs, t = fft(iq, self.sample_rate, self.center_freq,
                              NFFT, detrend, noverlap)

            # Спектр
            psd = P.mean(axis=1)
            self.ax1.plot(freqs, psd)
            self.ax1.grid(True)
            self.ax1.set_ylabel('dB', rotation=0, labelpad=10, loc='top', fontdict=font)
            self.ax1.set_xlim(freqs[0], freqs[-1])

            # Спектрограмма
            spectrogram = P.T
            pad_xextent = NFFT / self.sample_rate / 2
            xextent = np.min(t) - pad_xextent, np.max(t) + pad_xextent
            tmin, tmax = xextent
            extent = freqs[0], freqs[-1], tmin, tmax
            self.ax2.imshow(spectrogram, extent=extent, aspect='auto')
            # self.ax2.set_xlabel('Частота (МГц)', fontdict=font)
            self.ax2.yaxis.set_ticks([])  # удаление отметок

        return self.fig


def get_sdr(provider: str) -> SDR:
    global SDR_REGISTRY
    if provider not in SDR_REGISTRY:
        raise ValueError(
            f"No sdr registered with provider {provider}"
        )
    return SDR_REGISTRY[provider]


def list_sdr():
    global SDR_REGISTRY
    return [provider for provider in SDR_REGISTRY]
