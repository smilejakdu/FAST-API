from pydantic import BaseModel

from shared.core_response import CoreResponse


# {
#       "id": 21,
#       "title": "board_test",
#       "content": "board_one",
#       "user_id": 7,
#       "created_at": "2023-05-27T11:54:21.467216",
#       "updated_at": "2023-05-27T17:53:42.340217"
#       "deleted_at": null,
#     },
class BoardBase(BaseModel):
    id: int
    title: str
    content: str
    email: str
    user_id: int
    created_at: str
    updated_at: str | None = None
    deleted_at: str | None = None


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
