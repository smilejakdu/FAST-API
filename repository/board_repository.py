from sqlalchemy.orm import Session

from controller.dto.board_controller_dto.board_request_dto import BoardDto
from models.user_entity import user_entity
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


async def find_board_all(db: Session):
    # 페이지네이션 구현
    board = db.query(board_entity).all()
    return board


async def find_board_by_search(
        db: Session,
        page: int,
        page_size: int,
        search: str) -> object:
    if search:
        return (db.query(
            board_entity,
            user_entity,
        )
                .join(user_entity, user_entity.id == board_entity.user_id)
                .filter(board_entity.title.like(f"%{search}%"))
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all())
    return (db.query(
        board_entity,
        user_entity.email,
    )
            .join(
        user_entity,
        user_entity.id == board_entity.user_id,
    )
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all())
