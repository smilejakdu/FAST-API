# main.py

from fastapi import FastAPI

from controller import (user_controller,
                        board_controller,
                        )

app = FastAPI()  # FastAPI 모듈

app.include_router(user_controller.router)
app.include_router(board_controller.router)


@app.get("/")
def index():
    return {
        "Python": "Framework",
    }
