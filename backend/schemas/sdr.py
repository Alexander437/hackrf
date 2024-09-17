from typing import Literal

from pydantic import BaseModel, Field


class SdrConfig(BaseModel):
    sample_rate_m: float
    center_freq_m: float
    driver: str
    version: str | None = None


class FFTConfig(BaseModel):
    NFFT: int
    detrend: Literal["linear", "mean", "none"]
    noverlap: int = Field(ge=0)
    mode: Literal['psd', 'complex', 'magnitude', 'angle', 'phase']
