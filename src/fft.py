import numpy as np
from matplotlib import mlab

from src.settings import settings

detrends = {
    "linear": mlab.detrend_linear,
    "mean": mlab.detrend_mean,
    "none": mlab.detrend_none
}


def fft(
    iq: np.ndarray,
    sample_rate: int,
    center_freq: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:

    detrend = detrends[settings.DETREND_FUNC]
    P, freqs, t = mlab._spectral_helper(x=iq, y=None, NFFT=settings.NFFT, Fs=sample_rate,
                                     detrend_func=detrend, noverlap=settings.NOVERLAP, mode='psd')
    freqs = (freqs + center_freq) / 1e6  # in MHz
    P = np.abs(P)
    # Если нужно перевести в dB
    P = 10. * np.log10(P)
    # При применении mlab.detrend_linear, частота посередине спектра была удалена
    P[settings.NFFT // 2, :] = P[settings.NFFT // 2 + 1, :]

    return P, freqs, t
