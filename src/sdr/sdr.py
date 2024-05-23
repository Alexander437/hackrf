from abc import ABC, abstractmethod

from src.sdr.schemas import SdrConfig

SDR_REGISTRY = {}


def register_sdr(provider: str, cls) -> None:
    global SDR_REGISTRY
    if provider in SDR_REGISTRY:
        raise ValueError(
            f"Error while registering class {cls.__name__}, already taken by {SDR_REGISTRY[provider].__name__}"
        )
    SDR_REGISTRY[provider] = cls


class SDR(ABC):
    @abstractmethod
    def read_samples(self):
        raise NotImplementedError


def get_sdr(sdr_config: SdrConfig) -> SDR:
    global SDR_REGISTRY
    if sdr_config.provider not in SDR_REGISTRY:
        raise ValueError(
            f"No sdr registered with provider {sdr_config.provider}"
        )
    sdr: SDR = SDR_REGISTRY[sdr_config.provider](**sdr_config.config)
    return sdr


def list_sdr():
    global SDR_REGISTRY
    return [
        {"provider": provider, "class": cls.__name__}
        for provider, cls in SDR_REGISTRY.items()
    ]
