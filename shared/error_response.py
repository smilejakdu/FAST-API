from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()


class CustomException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code


@app.exception_handler(CustomException)
async def unicorn_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "ok": False,
            "message": exc.message,
            "status_code": exc.status_code
        },
    )
