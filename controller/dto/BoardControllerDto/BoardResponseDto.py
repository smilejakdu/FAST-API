from pydantic import BaseModel


class BoardBase(BaseModel):
    title: str
    content: str | None = None


class BoardCreate(BoardBase):
    user_id: int


class Board(BoardBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
