from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from controller.dto.review_controller_dto.review_request_dto import ReviewDto
from models.connection import get_db
from models.review_entity import review_entity


class ReviewRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    async def create_review(self, board_id: int, body: ReviewDto, user_id: int):
        new_review = review_entity()
        new_review.content = body.content
        new_review.board_id = board_id
        new_review.user_id = user_id

        self.session.add(new_review)
        self.session.flush()
        self.session.commit()

        return new_review

    async def update_review(self, review_id: int, body: ReviewDto, user_id: int):
        found_review = self.session.query(review_entity).filter(review_entity.id == review_id).first()
        found_review.content = body.content
        found_review.user_id = user_id

        self.session.flush()
        self.session.commit()

        return {
            'id': found_review.id,
            'content': found_review.content,
            'user_id': found_review.user_id,
            'board_id': found_review.board_id,
            'created_at': found_review.created_at.isoformat() if found_review.created_at else None,
            'updated_at': found_review.updated_at.isoformat() if found_review.updated_at else None,
            'deleted_at': found_review.deleted_at.isoformat() if found_review.deleted_at else None,
        }

    async def delete_review(self, review_id: int, user_id: int):
        found_review = self.session.query(review_entity).filter(
            review_entity.id == review_id,
            review_entity.user_id == user_id,
        ).first()

        found_review.deleted_at = datetime.now()

        self.session.flush()
        self.session.commit()

        return {
            'id': found_review.id,
            'content': found_review.content,
            'user_id': found_review.user_id,
            'board_id': found_review.board_id,
            'created_at': found_review.created_at.isoformat() if found_review.created_at else None,
            'updated_at': found_review.updated_at.isoformat() if found_review.updated_at else None,
            'deleted_at': found_review.deleted_at.isoformat() if found_review.deleted_at else None,
        }
