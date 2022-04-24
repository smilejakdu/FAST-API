from pydantic import BaseModel


class BoardDto(BaseModel):
    title: str
    content: str
    user_id: int
