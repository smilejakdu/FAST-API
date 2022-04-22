import json
import bcrypt
import re
import jwt

from fastapi import HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import json

from starlette.responses import JSONResponse, Response

from config.connection import get_db
from controller.dto.UserControllerDto.UserRequestDto import UserDto
from repository import UserRepository


def find_user_by_id(user_id: int):
    db: Session = Depends(get_db)

    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="BAD REQUEST")
        user = UserRepository.find_user_by_id(db, user_id)
        return JSONResponse(
            status_code=200,
            content=user,
        )
    except Exception:
        raise HTTPException(status_code=400, detail="BAD REQUEST")


def create_user(body: UserDto):
    db: Session = Depends(get_db)

    try:
        if not body:
            raise HTTPException(status_code=400, detail="BAD REQUEST")

        user = UserRepository.find_user_by_email(db, body.email)
        if user:
            raise HTTPException(status_code=404, detail="EXIST USER")
        UserRepository.create_user(db, body)

        return {
            "ok": True,
            "status_code": 201,
            "message": "SUCCESS",
        }
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Bad Request")


def update_user(user_id: int, body: UserDto):
    db: Session = Depends(get_db)
    try:
        if not body:
            raise HTTPException(status_code=404, detail="does not found user")
        foundUser = UserRepository.find_user_by_id(db, user_id)
        if bcrypt.checkpw(body.password.encode('UTF-8'), foundUser["password"].encode('UTF-8')):
            responseUpdated = UserRepository.update_user_by_id(db, user_id, body)
            return responseUpdated
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Bad Request")
