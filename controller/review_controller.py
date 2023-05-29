from fastapi import APIRouter, Depends, Request
from requests import Session

from controller.dto.review_controller_dto.review_request_dto import ReviewDto
from controller.dto.review_controller_dto.review_response_dto import ResponseCreateReview, ResponseUpdateReview
from models.connection import get_db
from services import review_service
from shared.core_response import CoreResponse

router = APIRouter(
    prefix="/reviews",
    tags=["REVIEWS"]
)


@router.post(
    "/{board_id}",
    response_model=ResponseCreateReview,
    status_code=201,
    summary="리뷰 생성하기",
    description="리뷰 생성 한다."
)
async def create_review(request: Request, board_id: int, body: ReviewDto, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access-token")
    return await review_service.create_reviews(db, board_id, body, access_token)


@router.put(
    "/{review_id}",
    response_model=ResponseUpdateReview,
    status_code=200,
    summary="리뷰 수정",
    description="리뷰를 수정 한다."
)
async def update_review(request: Request, review_id: int, body: ReviewDto, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access-token")
    return await review_service.update_review(db, review_id, body, access_token)


@router.delete(
    "/{review_id}",
    response_model=CoreResponse,
    status_code=200,
    summary="리뷰 삭제",
    description="리뷰를 삭제 한다."
)
async def delete_review(request: Request, review_id: int, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access-token")
    return await review_service.delete_review(db, review_id, access_token)
