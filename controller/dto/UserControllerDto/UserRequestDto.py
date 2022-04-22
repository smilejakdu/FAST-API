from pydantic import BaseModel


class UserDto(BaseModel):
    email: str
    nickname:str
    password: str
