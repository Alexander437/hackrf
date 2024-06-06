import asyncio
from hackrf import HackRF
from src.sdr.sdr import SDR


class HackrfSDR(SDR):
    def __init__(self, sample_rate: int, center_freq: float):
        self.hrf = HackRF()
        self.set_sample_rate(sample_rate)
        self.set_center_freq(center_freq)

    def read_samples(self):
        return self.hrf.read_samples()

    def set_sample_rate(self, sample_rate: int):
        self.sample_rate = sample_rate
        self.hrf.sample_rate = sample_rate

    def set_center_freq(self, center_freq: float):
        self.center_freq = center_freq
        self.hrf.center_freq = center_freq
