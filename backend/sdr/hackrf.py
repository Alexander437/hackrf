import time
import threading

import numpy as np
from hackrf import HackRF

from backend.sdr.sdr import SDR


class HackrfSDR(SDR):
    def __init__(self, sample_rate_m: float, center_freq_m: float):
        super().__init__()
        self.locker = threading.RLock()
        self.initialize_device(
            sample_rate_m=sample_rate_m,
            center_freq_m=center_freq_m,
        )

    def initialize_device(self, sample_rate_m: float, center_freq_m: float):
        with self.locker:
            self.hrf = HackRF()
            self.set_sample_rate(sample_rate_m)
            self.set_center_freq(center_freq_m)

    def read_samples(self) -> np.ndarray | None:
        try:
            with self.locker:
                return self.hrf.read_samples()
        except OSError:
            print("Failed to read samples")
            time.sleep(2)
            self.hrf.close()
            self.initialize_device(
                sample_rate_m=self.sample_rate,
                center_freq_m=self.center_freq,
            )
            return None

    def set_sample_rate(self, sample_rate_m: float):
        self.sample_rate = sample_rate_m * 1e6
        try:
            self.hrf.sample_rate = self.sample_rate
        except IOError:
            print("Failed to set sample rate")
            time.sleep(2)
            self.hrf.close()
            self.initialize_device(
                sample_rate_m=self.sample_rate,
                center_freq_m=self.center_freq,
            )

    def set_center_freq(self, center_freq_m: float):
        try:
            self.center_freq = center_freq_m * 1e6
            self.hrf.center_freq = self.center_freq
        except IOError:
            print("Failed to set sample rate")
            time.sleep(2)
            self.hrf.close()
            self.initialize_device(
                sample_rate_m=self.sample_rate,
                center_freq_m=self.center_freq,
            )
