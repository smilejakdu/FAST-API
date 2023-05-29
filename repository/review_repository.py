from datetime import datetime

from sqlalchemy.orm import Session

from controller.dto.review_controller_dto.review_request_dto import ReviewDto
from models.review_entity import review_entity


async def create_review(db: Session, board_id: int, body: ReviewDto, user_id: int):
    new_review = review_entity()
    new_review.content = body.content
    new_review.board_id = board_id
    new_review.user_id = user_id

    db.add(new_review)
    db.flush()
    db.commit()

    return new_review


async def update_review(db: Session, review_id: int, body: ReviewDto, user_id: int):
    found_review = db.query(review_entity).filter(review_entity.id == review_id).first()
    found_review.content = body.content
    found_review.user_id = user_id

    db.flush()
    db.commit()

    return {
        'id': found_review.id,
        'content': found_review.content,
        'user_id': found_review.user_id,
        'board_id': found_review.board_id,
        'created_at': found_review.created_at.isoformat() if found_review.created_at else None,
        'updated_at': found_review.updated_at.isoformat() if found_review.updated_at else None,
        'deleted_at': found_review.deleted_at.isoformat() if found_review.deleted_at else None,
    }


async def delete_review(db: Session, review_id: int, user_id: int):
    found_review = db.query(review_entity).filter(
        review_entity.id == review_id,
        review_entity.user_id == user_id,
    ).first()

    found_review.deleted_at = datetime.now()

    db.flush()
    db.commit()

    return {
        'id': found_review.id,
        'content': found_review.content,
        'user_id': found_review.user_id,
        'board_id': found_review.board_id,
        'created_at': found_review.created_at.isoformat() if found_review.created_at else None,
        'updated_at': found_review.updated_at.isoformat() if found_review.updated_at else None,
        'deleted_at': found_review.deleted_at.isoformat() if found_review.deleted_at else None,
    }
