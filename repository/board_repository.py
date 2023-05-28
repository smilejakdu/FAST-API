from datetime import datetime
from typing import Optional, Dict, Any

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


async def find_board_by_id(db: Session, board_id: int):
    return db.query(board_entity).filter(board_entity.id == board_id).first()


async def update_board(
    db: Session,
    board_id: int,
    body: BoardDto,
    user_id: int
):
    board = db.query(board_entity).filter(
        board_entity.id == board_id,
        board_entity.user_id == user_id,
    ).first()

    board.title = body.title
    board.content = body.content
    db.flush()
    db.commit()

    return {
        'id': board.id,
        'title': board.title,
        'content': board.content,
        'user_id': board.user_id,
        'created_at': board.created_at.isoformat() if board.created_at else None,
        'updated_at': board.updated_at.isoformat() if board.updated_at else None,
        'deleted_at': board.deleted_at.isoformat() if board.deleted_at else None,
    }


async def find_board_all(db: Session):
    # 페이지네이션 구현
    board = db.query(board_entity).all()
    return board


async def find_board_by_search(
    db: Session,
    page: Optional[int],
    page_size: Optional[int],
    search: Optional[str] = None,
):
    if search:
        return (db.query(
            board_entity,
            user_entity.email,
        )
                .join(user_entity, user_entity.id == board_entity.user_id)
                .filter(board_entity.title.like(f"%{search}%"))
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all())
    return (db.query(board_entity, user_entity.email)
            .join(user_entity, user_entity.id == board_entity.user_id)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all())


async def find_my_board(
    db: Session,
    email: str,
    page: Optional[int],
    page_size: Optional[int],
    search: Optional[str] = None,
):
    if search:
        return (db.query(board_entity)
                .join(user_entity, user_entity.id == board_entity.user_id)
                .filter(
            user_entity.email == email,
            board_entity.title.like(f"%{search}%"))
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all())
    return (db.query(board_entity)
            .join(user_entity, user_entity.id == board_entity.user_id)
            .filter(user_entity.email == email)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all())


async def delete_board(
    db: Session,
    board_id: int,
    user_id: int,
):
    board = db.query(board_entity).filter(
        board_entity.id == board_id,
        board_entity.user_id == user_id,
    ).first()

    board.deleted_at = datetime.now()
    db.flush()
    db.commit()

    return {
        'id': board.id,
        'title': board.title,
        'content': board.content,
        'user_id': board.user_id,
        'created_at': board.created_at.isoformat() if board.created_at else None,
        'updated_at': board.updated_at.isoformat() if board.updated_at else None,
        'deleted_at': board.deleted_at.isoformat() if board.deleted_at else None,
    }
