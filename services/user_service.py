from datetime import datetime, timedelta
from http import HTTPStatus
from typing import TypedDict

import bcrypt
import jwt
from fastapi import HTTPException, status, Depends
from jwt import decode
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from controller.dto.user_controller_dto.user_request_dto import LoginRequestDto, CreateRequestDto, UpdateRequestDto
from my_settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from repository.user_repository import UserRepository
from shared.login_check import login_check


class TokenData(TypedDict):
    sub: str


async def find_user_by_id(self, user_id: int):
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="BAD REQUEST")
        user = await self.user_repo.find_user_by_id(user_id)
        return JSONResponse(content=user)
    except Exception:
        raise HTTPException(status_code=400, detail="BAD REQUEST")


async def find_user_all(self):
    try:
        users = await self.user_repo.find_user_all()
        print('user:', users)
        return JSONResponse(content=users)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="BAD REQUEST")


async def create_user(
    body: CreateRequestDto,
    user_repo: UserRepository = Depends()
):
    try:
        if not body:
            raise HTTPException(status_code=400, detail="BAD REQUEST")
        user = await user_repo.find_user_by_email(body.email)
        if user:
            raise HTTPException(status_code=404, detail="EXIST USER")
        response_created_user = await user_repo.create_user(body)

        access_token = create_access_token({"email": body.email})
        response_created_user["access_token"] = access_token

        return {
            "ok": True,
            "status_code": 201,
            "message": response_created_user['message']
        }
    except Exception as e:
        print(e)
        # TODO: 여기서 rollback 구현할것
        raise HTTPException(status_code=400, detail="Bad Request")


async def create_access_token(
    data: TokenData,
    expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def login_user(
    body: LoginRequestDto,
    user_repo: UserRepository = Depends()
):
    try:
        found_user = user_repo.find_user_by_email(body.email)
        if not found_user:
            return JSONResponse({
                "ok": False,
                "status_code": 401,
                "message": "does not found user",
            })

        if not bcrypt.checkpw(body.password.encode('UTF-8'),
                              found_user["password"].encode('UTF-8')):
            return JSONResponse({
                "ok": False,
                "status_code": 401,
                "message": "Incorrect email or password",
            })

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": body.email},
            expires_delta=access_token_expires
        )
        del found_user["password"]

        response = JSONResponse({
            "ok": True,
            "status_code": HTTPStatus.OK,
            "message": "Login successful",
            "access_token": access_token,
            "data": found_user,
        })

        response.set_cookie(key="access-token", value=access_token)  # Set the cookie here
        return response
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="bad request",
        )


async def my_info(
    db: Session,
    access_token: str
):
    try:
        found_user = await login_check(db, access_token)

        del found_user["password"]
        response = JSONResponse({
            "ok": True,
            "status_code": HTTPStatus.OK,
            "message": "Login successful",
            "data": found_user,
        })
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Unauthorized")


async def update_user(
    body: UpdateRequestDto,
    access_token: str,
    user_repo: UserRepository = Depends(),
):
    try:
        payload = decode(
            access_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        email_from_token = payload.get("sub")
        print('email_from_token:', email_from_token)
        user_info = user_repo.find_user_by_email(email_from_token)
        print('user_info:', user_info)
        # body 에 있는 password 와 user_info 의 password 를 비교한다.
        if bcrypt.checkpw(
            body.password.encode('UTF-8'),
            user_info["password"].encode('UTF-8'),
        ):
            response_updated = user_repo.update_user_by_email(user_info['id'], body)
            return response_updated
    except Exception as e:
        print(e)
        # db.rollback() -> TODO: rollback 구현해야함
        raise HTTPException(status_code=400, detail="Bad Request")
