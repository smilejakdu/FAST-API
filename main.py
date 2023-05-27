# main.py

from fastapi import FastAPI
import uvicorn
from controller import (user_controller,
                        board_controller,
                        )

app = FastAPI()  # FastAPI 모듈

app.include_router(user_controller.router)
app.include_router(board_controller.router)


@app.get("/health")
def index():
    return 'health check ok'


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=13013)  # 기본 포트 8000
