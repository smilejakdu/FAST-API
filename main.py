# main.py

from fastapi import FastAPI
import uvicorn
from controller import (user_controller,
                        board_controller,
                        review_controller,
                        )
from fastapi.middleware.cors import CORSMiddleware

from shared.error_response import unicorn_exception_handler, CustomException

app = FastAPI()  # FastAPI 모듈

app.add_exception_handler(CustomException, unicorn_exception_handler)

origins = [
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
def health_check_handler():
    return 'health check ok'


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=13013)  # 기본 포트 8000
