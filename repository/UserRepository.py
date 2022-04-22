import json
import bcrypt
import re
import jwt
import requests

from sqlalchemy.orm import Session
from sqlalchemy import update

from controller.dto.UserControllerDto.UserRequestDto import UserDto
from models.UserEntity import UserEntity

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def create_user(db: Session, body):
    user = UserEntity()
    user.email = body.email
    user.nickname = body.nickname
    password_crypt = bcrypt.hashpw(body.password.encode('utf-8'),
                                   bcrypt.gensalt()).decode('utf-8')
    user.password = password_crypt
    user.is_active = True

    db.add(user)

    db.commit()

    return {
        "status_code": 201,
    }


def find_user_by_id(db: Session, user_id: int):
    user = db.query(UserEntity).filter(UserEntity.id == user_id).first()
    return jsonable_encoder(user)


def find_user_by_email(db: Session, user_email: str):
    user = db.query(UserEntity).filter(UserEntity.email == user_email).first()
    return jsonable_encoder(user)


def update_user_by_id(db: Session, user_id: int, body: UserDto):
    stmt = update(UserEntity).where(UserEntity.id == user_id).values(nickname=body.nickname).\
        execution_options(synchronize_session="fetch")
    db.execute(stmt)
    db.commit()
    return {
        "ok": True,
        "status_code": 200,
        "data": user_id,
        "message": "SUCCESS",
    }
