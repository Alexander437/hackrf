import asyncio
import random

import numpy as np
from websockets import ConnectionClosedError
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.fft import fft
from src.settings import settings
from src.sdr.sdr import get_sdr

router = APIRouter(
    prefix="/sdr",
    tags=["sdr"],
)

sdr = get_sdr("HackRF")


@router.post("/set_center_freq")
def set_center_freq(center_freq_m: int):
    try:
        sdr.set_center_freq(center_freq_m)
        return {"center_freq": sdr.center_freq, "error": ""}
    except Exception as e:
        return {"error": str(e), "center_freq": sdr.center_freq}


@router.websocket("/ws")
async def get_spectrum(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            iq = sdr.read_samples()
            if iq is None:
                print("No samples")
                continue

            P, freqs, t = fft(iq, sdr.sample_rate, sdr.center_freq * 1e6,
                              settings.INIT_NFFT, settings.INIT_DETREND_FUNC, settings.INIT_NOVERLAP)
            await ws.send_json({"psd": list(P.mean(axis=1) + random.random()), "freqs": list(freqs)})
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except ConnectionClosedError:
        print("Connection closed")
