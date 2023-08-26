from typing import Optional

from pydantic import BaseModel

from controller.dto.board_controller_dto.board_response_dto import Board
from shared.core_response import CoreResponse


class UserBase(BaseModel):
    email: str


class LoginResponse(CoreResponse):
    data: str
    access_token: Optional[str] = None


class MyInfoResponse(CoreResponse):
    data: str


class UpdateUserResponse(CoreResponse):
    data: object


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Board] = []

    class Config:
        orm_mode = True
