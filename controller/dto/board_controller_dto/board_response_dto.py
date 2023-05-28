from datetime import datetime

from pydantic import BaseModel

from shared.core_response import CoreResponse


class BoardBase(BaseModel):
    id: int
    title: str
    content: str
    email: str
    user_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class ResponseCreateBoard(CoreResponse):
    data: BoardBase


class ResponseFindBoardAll(CoreResponse):
    data: list[BoardBase]

    class Config:
        orm_mode = True


class Board(BoardBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
