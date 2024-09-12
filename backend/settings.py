import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    # SDR initial config
    INIT_SAMPLE_RATE_M: int = os.getenv("INIT_SAMPLE_RATE", 20)
    INIT_CENTER_FREQ_M: int = os.getenv("INIT_CENTER_FREQ", 80)
    # FFT config
    INIT_NFFT: int = os.getenv("INIT_NFFT", 256)
    INIT_DETREND_FUNC: str = os.getenv("INIT_DETREND_FUNC", "linear")
    INIT_NOVERLAP: int = int(os.getenv("INIT_NOVERLAP", "0"))
    INIT_NOVERLAP = max(0, INIT_NOVERLAP)

    if INIT_DETREND_FUNC not in ["linear", "mean", "none"]:
        raise ValueError("DETREND_FUNC may be `linear`, `mean` or `none`")


settings = Settings()
