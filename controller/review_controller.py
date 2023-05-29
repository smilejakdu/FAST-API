from fastapi import APIRouter, Depends, Request
from requests import Session

from controller.dto.review_controller_dto.review_request_dto import ReviewDto
from models.connection import get_db
from services import review_service

router = APIRouter(
    prefix="/reviews",
    tags=["REVIEWS"]
)


@router.post(
    "",
    status_code=201,
    summary="리뷰 생성하기",
    description="리뷰 생성 한다."
)
async def create_review(request: Request, body: ReviewDto, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access-token")
    return await review_service.create_reviews(db, body, access_token)
