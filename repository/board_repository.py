from sqlalchemy.orm import Session

from controller.dto.board_controller_dto.board_request_dto import BoardDto
from models.board_entity import board_entity


async def create_board(db: Session, body: BoardDto, user_id: int):
    new_board = board_entity()
    new_board.title = body.title
    new_board.content = body.content
    new_board.user_id = user_id

    db.add(new_board)
    db.flush()
    db.commit()

    return new_board