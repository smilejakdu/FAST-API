import bcrypt
import jwt
from datetime import datetime, timedelta

from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session

from starlette.responses import JSONResponse

from models.connection import get_db
from controller.dto.UserControllerDto.UserRequestDto import loginRequestDto, createRequestDto, updateRequestDto
from my_settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
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


def find_user_all():
    db: Session = Depends(get_db)
    try:
        users = UserRepository.find_user_all(db)
        return JSONResponse(
            status_code=200,
            content=users,
        )
    except Exception:
        raise HTTPException(status_code=400, detail="BAD REQUEST")


def create_user(body: createRequestDto):
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


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def login_user(body: loginRequestDto):
    db: Session = Depends(get_db)

    try:
        foundUser = UserRepository.find_user_by_email(db, body.email)
        if bcrypt.checkpw(body.password.encode('UTF-8'),
                          foundUser["password"].encode('UTF-8')):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub": body.email}, expires_delta=access_token_expires)
            return {
                "ok": True,
                "status_code": 200,
                "data": foundUser["email"],
                "access_token": access_token,
                "token_type": "bearer"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="bad request",
        )


def update_user(user_id: int, body: updateRequestDto):
    db: Session = Depends(get_db)
    try:
        if not body:
            raise HTTPException(status_code=404, detail="does not found user")
        found_user = UserRepository.find_user_by_id(db, user_id)
        if bcrypt.checkpw(body.password.encode('UTF-8'), found_user["password"].encode('UTF-8')):
            response_updated = UserRepository.update_user_by_id(db, user_id, body)
            return response_updated
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Bad Request")
