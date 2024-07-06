import json
import os
import signal
from typing import Dict, Any

import fastapi
import numpy as np
from fastapi import APIRouter
from starlette.requests import Request
from sse_starlette.sse import EventSourceResponse

from src.logger import logger
from src.sdr.sdr import get_sdr
from src.sdr.schemas import SubscribeRequest, UnsubscribeRequest

router = APIRouter(
    prefix="/api",
    tags=["sdr"],
)

sdr = get_sdr("JScanner")

BUFFER = dict()
NUM_SAVES = 7
MESSAGE_STREAM_RETRY_TIMEOUT = 15000  # millisecond


def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return fastapi.Response(status_code=200, content='Server shutting down...')


@router.post("/write_file")
def write_file(class_name: str, id: int, srcName: str):
    global BUFFER
    dir_name = f"./app/data/{class_name}"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    num = len(os.listdir(dir_name))
    BUFFER[id]["save_status"] = {
        "count": NUM_SAVES,
        "file": f"{dir_name}/{num}.npz",
        "srcName": srcName,
        "data": []
    }
    return {"ok": "Ok", "message": f"Идет запись в файл {dir_name}/{num}.npz ..."}


@router.post("/sub")
def sub(recv: SubscribeRequest):
    logger.info(f"Subscription to ({recv.id}) {recv.leftFreq} - {recv.rightFreq}")
    global BUFFER
    BUFFER[recv.id] = {
        "data": [],
        "save_status": {
            "count": 0,
            "file": None,
            "srcName": None,
            "data": None
        }
    }
    sdr.subscribe(recv)
    return {"status": "ok"}


@router.post("/unsub")
def unsub(recv: UnsubscribeRequest):
    global BUFFER
    for id in recv.graphId:
        try:
            del BUFFER[id]
        except:
            pass
        finally:
            logger.info(f"Unsubscription ({id})")
    sdr.unsubscribe(recv)
    return {"status": "ok"}


@router.post("/global/graph")
def receive_data(inp: Dict[Any, Any]):
    global BUFFER
    id = inp.get("id")
    if id in BUFFER:
        BUFFER[id]["data"].append(inp)
        if BUFFER[id]["save_status"]["count"] > 0:
            BUFFER[id]["save_status"]["count"] -= 1
            BUFFER[id]["save_status"]["data"].append(inp["powerArray"]["data"])
            if BUFFER[id]["save_status"]["count"] == 0:
                try:
                    np.savez_compressed(
                        BUFFER[id]["save_status"]["file"],
                        leftFreq=inp["leftFreq"], rightFreq=inp["rightFreq"],
                        step=inp["step"], width=inp["width"],
                        data=BUFFER[id]["save_status"]["data"],
                        method=BUFFER[id]["save_status"]["srcName"]
                    )
                    logger.info(f"Saved data in {BUFFER[id]['save_status']['file']}")
                except Exception as e:
                    logger.error(e)
                BUFFER[id]["save_status"] = {
                    "count": 0,
                    "file": None,
                    "srcName": None,
                    "data": None
                }


@router.get("/stream")
async def sse(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                logger.info("Request disconnected")
                break

            try:
                for event_id, value in BUFFER.items():
                    if len(value["data"]) > 0:
                        yield {
                            "event": event_id,
                            "id": "message_id",
                            "retry": MESSAGE_STREAM_RETRY_TIMEOUT,
                            "data": json.dumps(value["data"][-1]),
                        }
                        value["data"].clear()
                    else:
                        continue
            except RuntimeError as e:
                continue

    return EventSourceResponse(event_generator())
