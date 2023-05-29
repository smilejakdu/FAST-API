from fastapi import HTTPException
from http import HTTPStatus
from requests import Session

from controller.dto.review_controller_dto.review_request_dto import ReviewDto
from repository import review_repository
from starlette.responses import JSONResponse

from shared.login_check import login_check


async def create_reviews(db: Session, board_id: int, body: ReviewDto, access_token: str):
    if not body:
        raise HTTPException(status_code=400, detail="review 값을 입력해주세요")

    try:
        found_user = await login_check(db, access_token)
        if not found_user:
            raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")

        response_created_review = await review_repository.create_review(
            db,
            board_id,
            body,
            found_user["id"],
        )

        data = {
            'id': response_created_review.id,
            'content': response_created_review.content,
            'email': found_user['email'],
            'created_at': str(response_created_review.created_at),  # assuming this is a datetime object
            'updated_at': str(response_created_review.updated_at),  # assuming this is a datetime object
            'deleted_at': str(response_created_review.deleted_at) if response_created_review.deleted_at else None,
        }

        return JSONResponse({
            "ok": True,
            "status_code": HTTPStatus.OK,
            "message": "Create Board Successful",
            "data": data,
        })
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


async def update_review(db: Session, review_id: int, body: ReviewDto, access_token: str):
    if not body:
        raise HTTPException(status_code=400, detail="review 값을 입력해주세요")

    try:
        found_user = await login_check(db, access_token)
        if not found_user:
            raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")

        response_updated_review = await review_repository.update_review(
            db,
            review_id,
            body,
            found_user["id"],
        )

        return JSONResponse({
            "ok": True,
            "status_code": HTTPStatus.OK,
            "message": "Update Board Successful",
            "data": response_updated_review,
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def delete_review(db: Session, review_id: int, access_token: str):
    try:
        found_user = await login_check(db, access_token)
        if not found_user:
            raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")

        response_deleted_review = await review_repository.delete_review(
            db,
            review_id,
            found_user["id"],
        )

        return JSONResponse({
            "ok": True,
            "status_code": HTTPStatus.OK,
            "message": "Delete Review Successful",
            "data": response_deleted_review,
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
