from abc import ABC, abstractmethod

from src.sdr.schemas import SubscribeRequest
from src.sdr.schemas import UnsubscribeRequest

SDR_REGISTRY = {}


def register_sdr(provider: str, cls) -> None:
    global SDR_REGISTRY
    if provider in SDR_REGISTRY:
        raise ValueError(
            f"Error while registering class {cls.__name__}, already taken by {SDR_REGISTRY[provider].__name__}"
        )
    SDR_REGISTRY[provider] = cls()


class SDR(ABC):

    @abstractmethod
    async def subscribe(self, recv: SubscribeRequest):
        raise NotImplementedError
    @abstractmethod
    async def unsubscribe(self, recv: UnsubscribeRequest):
        raise NotImplementedError

def get_sdr(provider: str) -> SDR:
    global SDR_REGISTRY
    if provider not in SDR_REGISTRY:
        raise ValueError(
            f"No sdr registered with provider {provider}"
        )
    return SDR_REGISTRY[provider]


def list_sdr():
    global SDR_REGISTRY
    return [provider for provider in SDR_REGISTRY]
