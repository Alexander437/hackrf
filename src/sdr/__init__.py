"""
from src.sdr.sdr import get_sdr, list_sdr

list_sdr()
hrf = get_sdr("HackRF")
res = hrf.get_graphs()
res.show()

"""
from src.sdr.hackrf import HackrfSDR
from src.sdr.sdr import register_sdr, get_sdr, list_sdr

register_sdr("HackRF", HackrfSDR)
