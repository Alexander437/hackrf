from hackrf import HackRF
from src.sdr.sdr import SDR


class HackrfSDR(SDR):
    def __init__(self, sample_rate_m: int, center_freq_m: int):
        super().__init__()
        self.hrf = HackRF()
        self.set_sample_rate(sample_rate_m)
        self.set_center_freq(center_freq_m)

    def read_samples(self):
        try:
            return self.hrf.read_samples()
        except OSError:
            print("Failed to read samples")
            return None

    def stop(self):
        self.hrf.stop_rx()

    def set_sample_rate(self, sample_rate_m: int):
        self.sample_rate = sample_rate_m * 1e6
        self.hrf.sample_rate = self.sample_rate

    def set_center_freq(self, center_freq_m: int):
        self.center_freq = center_freq_m * 1e6
        self.hrf.center_freq = self.center_freq
