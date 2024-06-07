import numpy as np
from matplotlib import mlab

detrends = {
    "linear": mlab.detrend_linear,
    "mean": mlab.detrend_mean,
    "none": mlab.detrend_none
}


def fft(
    iq: np.ndarray,
    sample_rate: int,
    center_freq: int,
    NFFT: int,
    detrend: str,
    noverlap: int

) -> tuple[np.ndarray, np.ndarray, np.ndarray]:

    detrend_func = detrends[detrend]
    P, freqs, t = mlab._spectral_helper(x=iq, y=None, NFFT=NFFT, Fs=sample_rate,
                                     detrend_func=detrend, noverlap=noverlap, mode='psd')
    freqs = (freqs + center_freq) / 1e6  # in MHz
    P = np.abs(P)
    # Если нужно перевести в dB
    P = 10. * np.log10(P)
    # При применении mlab.detrend_linear, частота посередине спектра была удалена
    if NFFT > 10:
        P[NFFT // 2, :] = P[NFFT // 2 + 1, :]

    return P, freqs, t
