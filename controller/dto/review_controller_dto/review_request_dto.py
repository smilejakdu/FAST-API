from pydantic import BaseModel, Field


class ReviewDto(BaseModel):
    content: str = Field(..., description="Review content")
