from pydantic import BaseModel, Field


class ReviewDto(BaseModel):
    board_id: int = Field(..., description="Board id")
    content: str = Field(..., description="Review content")
