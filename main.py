# main.py

from fastapi import FastAPI

from controller import TestController, UserController

app = FastAPI()  # FastAPI 모듈

app.include_router(TestController.router)
app.include_router(UserController.router)


@app.get("/")
def index():
    return {
        "Python": "Framework",
    }
