from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(BaseModel):
    email: str


class UserDto(UserBase):
    nickname: str
    password: str


class CreateRequestDto(BaseModel):
    email: EmailStr
    nickname: str
    password: str


class LoginRequestDto(BaseModel):
    email: str
    password: str


class UpdateRequestDto(BaseModel):
    email: str
    nickname: str
    password: str
