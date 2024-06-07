import numpy as np
from matplotlib import mlab, pyplot as plt

plt.style.use('./mpl_styles/light.mplstyle')

center_freq = 88.5e6
NFFT = 256
sample_rate = 20e6

signals = np.load("data/example.npz")
iq = signals["arr_0"]

P, freqs, t = mlab._spectral_helper(x=iq, y=None, NFFT=NFFT, Fs=sample_rate,
                                     detrend_func=None, noverlap=0, mode='psd')

freqs = (freqs + center_freq) / 1e6  # in MHz
P = np.abs(P)
# Если нужно перевести в dB
P = 10. * np.log10(P)

fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(10, 10))

# Спектр
psd = P.mean(axis=1)
ax1.plot(freqs, psd)  # in MHz
ax1.grid(True)
ax1.set_xlim(freqs[0], freqs[-1])
ax1.set_ylabel('dB', rotation=0)

# Спектрограмма
spectrogram = P.T
pad_xextent = NFFT / sample_rate / 2
xextent = np.min(t) - pad_xextent, np.max(t) + pad_xextent
tmin, tmax = xextent
extent = freqs[0], freqs[-1], tmin, tmax
ax2.imshow(spectrogram, extent=extent, aspect='auto')
ax2.set_xlabel('Частота (МГц)')

plt.tight_layout()
plt.show()

