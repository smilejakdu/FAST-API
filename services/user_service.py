from datetime import datetime, timedelta
from http import HTTPStatus

import bcrypt
import jwt
from fastapi import HTTPException, status, Depends, Request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from controller.dto.user_controller_dto.user_request_dto import LoginRequestDto, CreateRequestDto, UpdateRequestDto
from my_settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from repository import user_repository
from repository.user_repository import UserRepository
from shared.error_response import CustomException


async def find_user_all(db: Session):
    try:
        users = await user_repository.find_user_all(db)
        print('user:', users)
        return JSONResponse(content=users)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="BAD REQUEST")


async def create_user(
    body: CreateRequestDto,
    user_repo: UserRepository,
):
    if not body:
        raise CustomException(message="BAD REQUEST", status_code=400)
    user = await user_repo.find_user_by_email(body.email)
    if user:
        raise CustomException(message="EXIST USER", status_code=409)
    response_created_user = await user_repo.create_user(body)

    access_token = await create_access_token({"email": body.email})
    response_created_user["access_token"] = access_token

    return {
        "ok": True,
        "status_code": 201,
        "message": response_created_user['message']
    }


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
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
    user_repo: UserRepository,
):
    try:
        found_user = await user_repo.find_user_by_email(body.email)
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
        access_token = await create_access_token(data={"sub": body.email}, expires_delta=access_token_expires)
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
    user: dict,
):
    try:
        del user["password"]
        return JSONResponse({
            "ok": True,
            "status_code": HTTPStatus.OK,
            "message": "Login successful",
            "data": user,
        })
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Unauthorized")


async def get_user_from_token(
    request: Request,
    user_repo: UserRepository = Depends(UserRepository)
):
    try:
        get_access_token = request.cookies.get('access-token', None)
        payload = jwt.decode(get_access_token, SECRET_KEY, algorithms=ALGORITHM)
        print(payload)
        user = await user_repo.find_user_by_email(payload['sub'])
        print('user:', user)
        return user
    except jwt.DecodeError:
        raise CustomException(message="INVALID_TOKEN", status_code=400)
    except KeyError:
        raise CustomException(message="INVALID_KEY", status_code=400)


async def update_user(
    body: UpdateRequestDto,
    user_repo: UserRepository,
    user: dict,
):
    try:
        if not bcrypt.checkpw(
            body.password.encode('UTF-8'),
            user["password"].encode('UTF-8'),
        ):
            raise CustomException(message="INVALID_PASSWORD", status_code=400)
        response_updated = await user_repo.update_user_by_email(user['id'], body)
        if response_updated['ok']:
            return {
                "ok": response_updated['ok'],
                "message": "SUCCESS",
                "status_code": 200,
                "data": body
            }

    except Exception as e:
        print(e)
        raise CustomException(message="BAD REQUEST", status_code=400)
