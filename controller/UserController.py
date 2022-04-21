# routes/test.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.connection import get_db
from controller.dto.UserControllerDto.UserRequestDto import UserDto
from services import UserService
from shared.CoreResponse import CoreResponse

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/find_user",response_model = CoreResponse, status_code = 200)
async def find_user(user_id: int, db: Session = Depends(get_db)):
    res = UserService.find_user(db, user_id)

    return {
        "res": res,
    }  # 결과


@router.post("", response_model=CoreResponse, status_code=201)
async def create_user(body: UserDto, db: Session = Depends(get_db)):
    return UserService.create_user(db, body)
