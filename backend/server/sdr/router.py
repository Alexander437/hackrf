import asyncio
import os
import signal
import aiofiles.os as aios

import fastapi
import numpy as np
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, Depends
from websockets import ConnectionClosedOK, ConnectionClosedError

from backend.sdr.sdr import get_sdr, sdr_registry, SDR

router = APIRouter(
    prefix="/sdr",
    tags=["sdr"],
)


def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return fastapi.Response(status_code=status.HTTP_200_OK, content='Server shutting down...')


@router.get("/list")
def get_list_sdr() -> list[dict]:
    return sdr_registry.keys()


@router.get("/info")
def get_driver_info(sdr: SDR = Depends(get_sdr)) -> dict:
    return sdr.get_info()


@router.post("/set_center_freq")
def set_center_freq(
        center_freq_m: float,
        sdr: SDR = Depends(get_sdr),
):
    sdr.set_center_freq(center_freq_m)
    return {"center_freq": center_freq_m, "error": ""}


@router.post("/set_sample_rate")
def set_sample_rate(
        sample_rate_m: float,
        sdr: SDR = Depends(get_sdr),
):
    sdr.set_sample_rate(sample_rate_m)
    return {"sample_rate": sample_rate_m, "error": ""}


@router.post("/write_file")
async def write_file(
        class_name: str,
        sdr: SDR = Depends(get_sdr),
):
    IQ = dict()
    dir_name = f"./app/data/{class_name}"
    if not await aios.path.exists(dir_name):
        await aios.makedirs(dir_name)

    for i in range(3):
        IQ[i] = sdr.read_samples()
        if IQ[i] is None:
            return {"ok": "Error", "message": "Не удалось прочитать данные!"}

    num = len(os.listdir(dir_name))
    try:
        np.savez_compressed(f"{dir_name}/{num}.npz", iq0=IQ[0], iq1=IQ[1], iq2=IQ[2],
                            center_freq=sdr.config.center_freq_m, sample_rate=sdr.config.sample_rate_m)
    except TypeError as e:
        return {"ok": "Ошибка", "message": str(e)}

    return {"ok": "Ok", "message": f"Файл {dir_name}/{num}.npz записан"}


@router.websocket("/ws")
async def get_spectrum(
        ws: WebSocket,
        sdr: SDR = Depends(get_sdr),
):
    await ws.accept()
    try:
        while True:
            psd = await sdr.aget_psd()
            if psd is None:
                continue
            await asyncio.sleep(0.1)
            await ws.send_json(psd)
    except (WebSocketDisconnect, ConnectionClosedOK):
        print("WebSocket disconnected")
    except ConnectionClosedError:
        print("Connection closed")
        await ws.close()
    except KeyboardInterrupt:
        await ws.close()
        shutdown()
