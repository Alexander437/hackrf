from pydantic import BaseModel


class SdrConfig(BaseModel):
    sample_rate_m: float
    center_freq_m: float
    driver: str
    version: str | None = None
