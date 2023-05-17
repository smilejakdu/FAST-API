from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from controller.dto.UserControllerDto.UserRequestDto import createRequestDto, updateRequestDto, loginRequestDto
from models.connection import get_db
from services import UserService
from shared.CoreResponse import CoreResponse

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/find_user", status_code=200)
async def find_user(user_id: int):
    return UserService.find_user_by_id(user_id)


@router.get("/find_user_all", status_code=200)
def find_user(db:Session = Depends(get_db)):
    return UserService.find_user_all(db)


@router.post("", response_model=CoreResponse, status_code=201)
async def create_user(body: createRequestDto):
    return UserService.create_user(body)


@router.post("/login", response_model=CoreResponse, status_code=200)
async def login_user(body: loginRequestDto):
    return UserService.login_user(body)


@router.put("/{user_id}", response_model=CoreResponse, status_code=200)
async def update_user(body: updateRequestDto, user_id: int):
    return UserService.update_user(user_id, body)
