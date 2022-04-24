# routes/test.py
from fastapi import APIRouter

from controller.dto.UserControllerDto.UserRequestDto import UserDto
from services import UserService
from shared.CoreResponse import CoreResponse

router = APIRouter(
    prefix = "/user",
    tags   = ["user"],
)


@router.get("/find_user", status_code=200)
async def find_user(user_id: int):
    return UserService.find_user_by_id(user_id)


@router.post("", response_model=CoreResponse, status_code=201)
async def create_user(body: UserDto):
    return UserService.create_user(body)


@router.put("/{user_id}", response_model=CoreResponse, status_code=200)
async def update_user(body: UserDto, user_id: int):
    return UserService.update_user(user_id, body)
