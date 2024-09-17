import numpy as np
from matplotlib import mlab

detrends = {
    "linear": mlab.detrend_linear,
    "mean": mlab.detrend_mean,
    "none": mlab.detrend_none
}


def fft(
        iq: np.ndarray,
        sample_rate_m: float,
        center_freq_m: float,
        NFFT: int,
        detrend: str,
        noverlap: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:

    detrend_func = detrends[detrend]
    P, freqs, t = mlab._spectral_helper(x=iq, y=None, NFFT=NFFT, Fs=(sample_rate_m * 1e6),
                                        detrend_func=detrend_func, noverlap=noverlap, mode='psd')

    freqs = freqs / 1e6 + center_freq_m  # in MHz
    # Перевод в dB
    P = 10. * np.log10(np.abs(P))

    return P, freqs, t
