from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from shared.core_response import CoreResponse


class ReviewBase(BaseModel):
    id: int
    board_id: int
    user_id: int
    content: str
    created_at: Optional[datetime] | None = None
    updated_at: Optional[datetime] | None = None
    deleted_at: Optional[datetime] | None = None


class ResponseCreateReview(CoreResponse):
    data: ReviewBase


class ResponseUpdateReview(CoreResponse):
    data: ReviewBase
