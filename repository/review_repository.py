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
