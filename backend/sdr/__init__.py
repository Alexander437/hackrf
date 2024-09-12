"""
from src.sdr.sdr import get_sdr, list_sdr

list_sdr()
hrf = get_sdr("HackRF")
res = hrf.get_graphs()
res.show()

"""
from backend.sdr.hackrf import HackrfSDR
from backend.sdr.sdr import register_sdr

register_sdr("HackRF", HackrfSDR)
