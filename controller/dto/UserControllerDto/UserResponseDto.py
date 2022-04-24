from pydantic import BaseModel


class BoardBase(BaseModel):
    title: str
    content: str | None = None


class BoardCreate(BoardBase):
    pass


class Board(BoardBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


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
