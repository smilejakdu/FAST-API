from pydantic import BaseModel, Field


class BoardDto(BaseModel):
    title: str = Field(..., description="Board title")
    content: str = Field(..., description="Board content")


class CreateBoardDto(BaseModel):
    title: str = Field(..., description="Board title")  # ... (ellipsis)를 사용하여 필드가 필수임을 명시적으로 표시
    content: str = Field(..., description="Board content")


class QueryFindBoardRequestDto(BaseModel):
    search: str = None


class FindBoardRequestDto(BaseModel):
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(10, ge=1, le=100, description="Page size (1-10)")
    search: str = Field(None, description="Search keyword")
