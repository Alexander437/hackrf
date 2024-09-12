import os
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.sdr.router import router as sdr_router

app = FastAPI()
app.mount("/app/static", StaticFiles(directory="app/static", html=True), name="static")


@app.get("/")
async def get_index_html():
    return FileResponse('app/static/index.html')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sdr_router)


def start(app: FastAPI | str = "backend.main:app"):
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    start(app=app)
