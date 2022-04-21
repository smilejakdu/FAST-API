# main.py

from fastapi import FastAPI

from controller import TestController

app = FastAPI()  # FastAPI 모듈
app.include_router(TestController.router)  # 다른 route파일들을 불러와 포함시킴


@app.get("/")
def index():
    return {
        "Python": "Framework",
    }
