# main.py

from fastapi import FastAPI
import uvicorn
from controller import (user_controller,
                        board_controller, review_controller,
                        )
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()  # FastAPI 모듈

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:13013",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_controller.router)
app.include_router(board_controller.router)
app.include_router(review_controller.router)


@app.get("/health")
def index():
    return 'health check ok'


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=13013)  # 기본 포트 8000
