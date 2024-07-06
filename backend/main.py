import subprocess

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware

from src.sdr.router import router as sdr_router

app = FastAPI()
app.mount("/app/static", StaticFiles(directory="app/static", html=True), name="static")


@app.get("/index")
async def read_index():
    return FileResponse('app/static/index.html')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sdr_router)


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    command = ["hypercorn", "main:app", "--worker-class", "trio"]
    subprocess.run(command)
