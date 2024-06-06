import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    # SDR initial config
    INIT_SAMPLE_RATE: int = os.getenv("INIT_SAMPLE_RATE", 20e6)
    INIT_CENTER_FREQ: float = os.getenv("INIT_CENTER_FREQ", 88.5e6)
    # FFT config
    NFFT: int = os.getenv("NFFT", 256)
    DETREND_FUNC: str = os.getenv("DETREND_FUNC", "linear")
    NOVERLAP: int = int(os.getenv("NOVERLAP", "0"))
    NOVERLAP = max(0, NOVERLAP)

    if DETREND_FUNC not in ["linear", "mean", "none"]:
        raise ValueError("DETREND_FUNC may be `linear`, `mean` or `none`")


settings = Settings()
