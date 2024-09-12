import os
import signal
import asyncio
import aiofiles.os as aios

import fastapi
import numpy as np
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websockets import ConnectionClosedOK, ConnectionClosedError

from backend.sdr.sdr import get_sdr

router = APIRouter(
    prefix="/sdr",
    tags=["sdr"],
)

sdr = get_sdr("HackRF")


def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return fastapi.Response(status_code=200, content='Server shutting down...')


@router.post("/set_center_freq")
def set_center_freq(center_freq_m: float):
    sdr.set_center_freq(center_freq_m)
    return {"center_freq": sdr.center_freq, "error": ""}


@router.post("/set_sample_rate")
def set_sample_rate(sample_rate_m: float):
    sdr.set_sample_rate(sample_rate_m)
    return {"sample_rate": sdr.sample_rate, "error": ""}


@router.post("/write_file")
async def write_file(class_name: str):
    IQ = dict()
    dir_name = f"./app/data/{class_name}"
    if not await aios.path.exists(dir_name):
        await aios.makedirs(dir_name)

    for i in range(3):
        IQ[i] = sdr.read_samples()
        if IQ[i] is None:
            return {"ok": "Error", "message": "Не удалось прочитать данные!"}

    num = len(os.listdir(dir_name))
    np.savez_compressed(f"{dir_name}/{num}.npz", iq0=IQ[0], iq1=IQ[1], iq2=IQ[2],
                        center_freq=sdr.center_freq, sample_rate=sdr.sample_rate)
    return {"ok": "Ok", "message": f"Файл {dir_name}/{num}.npz записан"}


@router.websocket("/ws")
async def get_spectrum(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            psd = sdr.get_psd()
            if psd is None:
                continue

            await ws.send_json(psd)
            await asyncio.sleep(0.01)
    except (WebSocketDisconnect, ConnectionClosedOK):
        print("WebSocket disconnected")
        # shutdown()
    except ConnectionClosedError:
        print("Connection closed")
        await ws.close()
        # shutdown()
    except KeyboardInterrupt:
        await ws.close()
        shutdown()
