from http import HTTPStatus

import bcrypt
from jwt import decode, InvalidTokenError
import jwt
from datetime import datetime, timedelta

from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session

from starlette.responses import JSONResponse

from models.connection import get_db
from controller.dto.user_controller_dto.user_request_dto import LoginRequestDto, CreateRequestDto, UpdateRequestDto
from my_settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from repository import user_repository


def find_user_by_id(db: Session, user_id: int):
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="BAD REQUEST")
        user = user_repository.find_user_by_id(db, user_id)
        return JSONResponse(content=user)
    except Exception:
        raise HTTPException(status_code=400, detail="BAD REQUEST")


def find_user_all(db: Session):
    try:
        users = user_repository.find_user_all(db)
        print('user:', users)
        return JSONResponse(content=users)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="BAD REQUEST")


async def create_user(body: CreateRequestDto, db: Session):
    try:
        if not body:
            raise HTTPException(status_code=400, detail="BAD REQUEST")
        user = user_repository.find_user_by_email(db, body.email)
        if user:
            raise HTTPException(status_code=404, detail="EXIST USER")
        response_created_user = await user_repository.create_user(db, body)

        access_token = create_access_token({"email": body.email})
        response_created_user["access_token"] = access_token

        return {
            "ok": True,
            "status_code": 201,
            "message": response_created_user['message']
        }
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=400, detail="Bad Request")


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def login_user(body: LoginRequestDto, db: Session):
    print('body:', body)
    try:
        found_user = user_repository.find_user_by_email(db, body.email)
        if bcrypt.checkpw(body.password.encode('UTF-8'),
                          found_user["password"].encode('UTF-8')):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = await create_access_token(data={"sub": body.email}, expires_delta=access_token_expires)

            response = JSONResponse({
                "ok": True,
                "status_code": HTTPStatus.OK,
                "message": "Login successful",
                "data": found_user["email"],
                "access_token": access_token,
            })

            response.set_cookie(key="access-token", value=access_token)  # Set the cookie here
            return response
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="bad request",
        )


async def my_info(db: Session, access_token: str):
    try:
        payload = decode(
            access_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        email_from_token = payload.get("sub")
        user_info = user_repository.find_user_by_email(db, email_from_token)
        del user_info["password"]
        response = JSONResponse({
            "ok": True,
            "status_code": HTTPStatus.OK,
            "message": "Login successful",
            "data": user_info,
        })
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Unauthorized")


async def update_user(
        db: Session,
        body: UpdateRequestDto,
        access_token: str,
):
    try:
        payload = decode(
            access_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        email_from_token = payload.get("sub")
        print('email_from_token:', email_from_token)
        user_info = user_repository.find_user_by_email(db, email_from_token)
        print('user_info:', user_info)
        # body 에 있는 password 와 user_info 의 password 를 비교한다.
        if bcrypt.checkpw(
                body.password.encode('UTF-8'),
                user_info["password"].encode('UTF-8'),
        ):
            response_updated = user_repository.update_user_by_email(db, user_info['id'], body)
            return response_updated
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=400, detail="Bad Request")
