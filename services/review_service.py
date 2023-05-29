from fastapi import HTTPException
from requests import Session

from controller.dto.review_controller_dto.review_request_dto import ReviewDto


async def create_reviews(db: Session, body: ReviewDto, access_token: str):
    if not body:
        raise HTTPException(status_code=400, detail="값을 입력해주세요")
