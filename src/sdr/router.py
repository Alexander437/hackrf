from typing import List
from fastapi import APIRouter, WebSocket


router = APIRouter(
    prefix="/sdr",
    tags=["sdr"],
)


