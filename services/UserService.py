from sqlalchemy.orm import Session

from fastapi import Header, HTTPException
from controller.dto.UserControllerDto.UserRequestDto import UserDto
from repository import UserRepository


def find_user(db: Session, user_id: int):
    user = UserRepository.find_user_by_id(db, user_id)
    return user


def create_user(db: Session, body: UserDto):
    try:
        if not body:
            raise HTTPException(status_code=400, detail="bAD rEQUEST")

        user = UserRepository.find_user_by_email(db, body.email)
        if user:
            print(user["email"])
            print(user["is_active"])
            raise HTTPException(status_code=404, detail="EXIST USER")
        UserRepository.create_user(db, body)

        return {
            "ok": True,
            "status_code": 201,
            "message": "SUCCESS",
        }
    except Exception:
        raise HTTPException(status_code=400, detail="Bad Request")
