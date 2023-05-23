from sqlalchemy.orm import Session

from models.board_entity import BoardEntity


def create_board(db: Session, body):
    new_board = BoardEntity()
    new_board.title = body.title
    new_board.content = body.content

    return {

    }
