from pydantic import BaseModel

from shared.core_response import CoreResponse


class BoardBase(BaseModel):
    title: str
    content: str | None = None
    email: str
    created_at: str | None = None


class BoardCreate(CoreResponse):
    # data 는 객체로 해줘
    data: BoardBase


class Board(BoardBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True