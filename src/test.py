from hackrf import HackRF
from pylab import *

hrf = HackRF()
hrf.sample_rate = 20e6
hrf.center_freq = 88.5e6


def read_samples():
    while True:
        print("Ok")
        yield hrf.read_samples()


for sample in read_samples():
    try:
        psd(sample, NFFT=1024, Fs=hrf.sample_rate / 1e6, Fc=hrf.center_freq / 1e6)
        xlabel('Frequency (MHz)')
        ylabel('Relative power (dB)')
        show()
    except KeyboardInterrupt:
        print('Interrupted')
