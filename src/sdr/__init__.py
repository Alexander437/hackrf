from src.sdr import *
from src.sdr.hackrf import HackrfSDR
from src.sdr.sdr import register_sdr

register_sdr("HackRF", HackrfSDR())
