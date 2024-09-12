from abc import ABC, abstractmethod

import numpy as np

from backend.sdr.fft import fft
from backend.settings import settings

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
    center_freq: float
    sample_rate: float

    @abstractmethod
    def read_samples(self) -> np.ndarray | None:
        raise NotImplementedError

    @abstractmethod
    def set_sample_rate(self, sample_rate_m: float):
        raise NotImplementedError

    @abstractmethod
    def set_center_freq(self, center_freq_m: float):
        raise NotImplementedError

    def get_psd(self) -> dict[str, list] | None:
        iq = self.read_samples()
        if iq is None:
            print("No samples")
            return

        p, freqs, t = fft(iq, self.sample_rate, self.center_freq,
                          settings.INIT_NFFT, settings.INIT_DETREND_FUNC, settings.INIT_NOVERLAP)
        
        return {
            "psd": p.mean(axis=1).tolist(),
            "freqs": freqs.tolist()
        }


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
