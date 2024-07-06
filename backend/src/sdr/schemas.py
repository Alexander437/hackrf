from typing import List, Dict

from pydantic import BaseModel, Field


class SubscribeRequest(BaseModel):
    id: int = Field(
        title="номер подписки. может быть несколько, пользователь сам выбирает ее номер",
        default=1,
    )
    sectorId: int = Field(
        title="номер сектора. оставить это значение",
        default=1,
    )
    srcName: str = Field(
        title="ins - мгновенная мощность, avg - средняя мощность за некоторое время, coh - средняя мощность, "
              "рассчитанная когерентным способом, max - максимальное значение за некоторый период времени, "
              "min - минимальное значение за некоторый период времени",
        default='ins',
    )
    targetFps: int = Field(
        title="требуемое количество данных, отправляемых в секунду. если требуемое количество больше фактически "
              "получаемых данных - предыдущие данные будут отправлены повторно. рекомендуется оставить = 1",
        default=1,
    )
    width: int = Field(
        title="количество элементов массива со значениями мощности (разрешение спектра по горизонтали)",
        default=50,
    )
    leftFreq: int = Field(
        title="левая частота в МГц > 0 МГц",
        ge=0
    )
    rightFreq: int = Field(
        title="правая частота в МГц < 6000 МГц",
        me=6000
    )


class UnsubscribeRequest(BaseModel):
    graphId: List[int] = Field(
        title="массив id подписок"
    )


class JServerResponce(BaseModel):
    id: int
    leftFreq: float
    rightFreq: float
    width: int
    step: float
    powerArray: Dict[str, List[float]]
