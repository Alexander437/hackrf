import asyncio
from hackrf import HackRF
from src.sdr.sdr import SDR


class HackrfSDR(SDR):
    def __init__(self, sample_rate: float, center_freq: float):
        self.hrf = HackRF()
        self.sample_rate = sample_rate
        self.center_freq = center_freq

    async def read_samples(self):
        while True:
            yield self.hrf.read_samples()
            await asyncio.sleep(0.1)
