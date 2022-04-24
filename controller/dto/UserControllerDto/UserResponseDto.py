from pydantic import BaseModel

from controller.dto.BoardControllerDto.BoardResponseDto import Board


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Board] = []

    class Config:
        orm_mode = True
