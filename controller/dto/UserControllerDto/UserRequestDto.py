from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserDto(UserBase):
    nickname: str
    password: str


class createRequestDto(BaseModel):
    email: str
    nickname: str
    password: str


class loginRequestDto(BaseModel):
    email: str
    password: str


class updateRequestDto(BaseModel):
    email: str
    nickname: str
    password: str
