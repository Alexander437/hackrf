import os
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    # SDR initial config
    INIT_SAMPLE_RATE_M: float = os.getenv("INIT_SAMPLE_RATE", 20)
    INIT_CENTER_FREQ_M: float = os.getenv("INIT_CENTER_FREQ", 20)
    # FFT config
    INIT_NFFT: int = os.getenv("INIT_NFFT", 256)
    INIT_DETREND_FUNC: Literal["linear", "mean", "none"] = os.getenv("INIT_DETREND_FUNC", "mean")
    INIT_NOVERLAP: int = int(os.getenv("INIT_NOVERLAP", "0"))
    INIT_NOVERLAP = max(0, INIT_NOVERLAP)


settings = Settings()
