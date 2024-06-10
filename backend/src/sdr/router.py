import os
import asyncio
import signal

import fastapi
import numpy as np
from websockets import ConnectionClosedError, ConnectionClosedOK
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.fft import fft
from src.settings import settings
from src.sdr.sdr import get_sdr

router = APIRouter(
    prefix="/sdr",
    tags=["sdr"],
)

sdr = get_sdr("HackRF")


def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return fastapi.Response(status_code=200, content='Server shutting down...')


@router.post("/set_center_freq")
def set_center_freq(center_freq_m: int):
    try:
        sdr.set_center_freq(center_freq_m)
        return {"center_freq": sdr.center_freq, "error": ""}
    except Exception as e:
        return {"center_freq": sdr.center_freq, "error": str(e)}


@router.post("/write_file")
def write_file(class_name: str):
    IQ = dict()
    dir_name = f"./app/data/{class_name}"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

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
            iq = sdr.read_samples()
            if iq is None:
                print("No samples")
                continue

            p, freqs, t = fft(iq, sdr.sample_rate, sdr.center_freq,
                              settings.INIT_NFFT, settings.INIT_DETREND_FUNC, settings.INIT_NOVERLAP)

            await ws.send_json({
                "psd": p.mean(axis=1).tolist(),
                "freqs": freqs.tolist()
            })
            await asyncio.sleep(0.01)
    except (WebSocketDisconnect, ConnectionClosedOK):
        await ws.close()
        print("WebSocket disconnected")
        await asyncio.sleep(1)
        shutdown()
    except ConnectionClosedError:
        print("Connection closed")
        await asyncio.sleep(1)
        shutdown()
