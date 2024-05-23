from typing import Optional, Dict

from pydantic import BaseModel, Field


class SdrConfig(BaseModel):
    provider: str = Field(
        title="Provider of the sdr",
    )
    config: Optional[Dict[str, float]] = Field(
        title="Configuration for the sdr", default={
            "sample_rate": 20e6,
            "center_freq": 88.5e6
        }
    )
