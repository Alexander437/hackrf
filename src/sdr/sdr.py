from abc import ABC, abstractmethod

import numpy as np
from matplotlib import pyplot as plt

from src.fft import fft
from src.settings import settings

plt.style.use('dark_background')
font = {'family': 'DejaVu Sans', 'weight': 500, 'size': 14}
SDR_REGISTRY = {}


def register_sdr(provider: str, cls) -> None:
    global SDR_REGISTRY
    if provider in SDR_REGISTRY:
        raise ValueError(
            f"Error while registering class {cls.__name__}, already taken by {SDR_REGISTRY[provider].__name__}"
        )
    SDR_REGISTRY[provider] = cls


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

    def get_graphs(self):

        iq = self.read_samples()
        P, freqs, t = fft(iq, self.sample_rate, self.center_freq)
        fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(10, 10),
                                       facecolor='#2b2b2b', gridspec_kw={'height_ratios': [1, 2]})

        # Спектр
        psd = P.mean(axis=1)
        ax1.plot(freqs, psd, color='cyan')  # in MHz
        ax1.grid(True, color='gray')
        ax1.set_ylabel('dB', rotation=0, labelpad=10, loc='top', color='white', fontdict=font)
        ax1.set_xlim(freqs[0], freqs[-1])

        # Спектрограмма
        spectrogram = P.T
        pad_xextent = settings.NFFT / self.sample_rate / 2
        xextent = np.min(t) - pad_xextent, np.max(t) + pad_xextent
        tmin, tmax = xextent
        extent = freqs[0], freqs[-1], tmin, tmax
        ax2.imshow(spectrogram, extent=extent, aspect='auto', cmap='winter')
        ax2.set_xlabel('Частота (МГц)', labelpad=15, color='white', fontdict=font)
        ax2.yaxis.set_ticks([])  # удаление отметок

        return fig


def get_sdr(provider: str) -> SDR:
    global SDR_REGISTRY
    if provider not in SDR_REGISTRY:
        raise ValueError(
            f"No sdr registered with provider {provider}"
        )
    sdr: SDR = SDR_REGISTRY[provider](
        sample_rate=settings.INIT_SAMPLE_RATE,
        center_freq=settings.INIT_CENTER_FREQ
    )
    return sdr


def list_sdr():
    global SDR_REGISTRY
    return [
        {"provider": provider, "class": cls.__name__}
        for provider, cls in SDR_REGISTRY.items()
    ]
