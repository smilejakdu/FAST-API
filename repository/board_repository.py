from datetime import datetime
from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from sqlalchemy import func

from controller.dto.board_controller_dto.board_request_dto import BoardDto
from models.board_entity import board_entity
from models.connection import get_db
from models.review_entity import review_entity
from models.user_entity import user_entity


class BoardRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    async def find_board_object(
        board: board_entity,
    ):
        return {
            'id': board.id,
            'title': board.title,
            'content': board.content,
            'user_id': board.user_id,
            'created_at': board.created_at.isoformat() if board.created_at else None,
            'updated_at': board.updated_at.isoformat() if board.updated_at else None,
            'deleted_at': board.deleted_at.isoformat() if board.deleted_at else None,
        }

    async def create_board(
        self,
        body: BoardDto,
        user_id: int,
    ):
        new_board = board_entity.create(
            title=body.title,
            content=body.content,
            user_id=user_id,
        )

        self.session.add(new_board)
        self.session.flush()
        self.session.commit()

        return new_board

    # 특정 게시판에 연결된 리뷰를 가져오는 경우
    async def find_board_by_id(
        self,
        board_id: int,
    ):
        board = self.session.query(board_entity) \
            .options(joinedload(board_entity.reviews)) \
            .filter(board_entity.id == board_id) \
            .first()
        return board

    async def update_board(
        self,
        board_id: int,
        body: BoardDto,
        user_id: int
    ):
        board = await self.session.query(board_entity).filter(
            board_entity.id == board_id,
            board_entity.user_id == user_id,
        ).first()

        board.title = body.title
        board.content = body.content
        self.session.flush()
        self.session.commit()

        return self.find_board_object(board)

    async def find_board_by_search(
        self,
        page: Optional[int],
        page_size: Optional[int],
        search: Optional[str] = None,
    ):
        if search:
            return (self.session.query(
                board_entity,
                user_entity.email,
            )
                    .join(user_entity, user_entity.id == board_entity.user_id)
                    .filter(board_entity.title.like(f"%{search}%"))
                    .offset((page - 1) * page_size)
                    .limit(page_size)
                    .all())
        return (self.session.query(board_entity, user_entity.email)
                .join(user_entity, user_entity.id == board_entity.user_id)
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all())

    async def find_my_board(
        self,
        email: str,
        page: Optional[int],
        page_size: Optional[int],
        search: Optional[str] = None,
    ):
        # 리뷰 카운트를 얻기 위한 서브쿼리 생성
        subquery = (
            self.session.query(review_entity.board_id, func.count(review_entity.id).label("review_count"))
            .group_by(review_entity.board_id)
            .subquery()
        )

        base_query = (
            self.session.query(board_entity, subquery.c.review_count)
            .join(user_entity, user_entity.id == board_entity.user_id)
            .outerjoin(subquery, subquery.c.board_id == board_entity.id)
            .filter(user_entity.email == email)
        )

        # 검색어가 제공된 경우
        if search:
            base_query = base_query.filter(board_entity.title.like(f"%{search}%"))

        results = (
            base_query
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return results

    async def delete_board(
        self,
        board_id: int,
        user_id: int,
    ):
        board = self.session.query(board_entity).filter(
            board_entity.id == board_id,
            board_entity.user_id == user_id,
        ).first()

        board.deleted_at = datetime.now()
        self.session.flush()
        self.session.commit()

        return self.find_board_object(board)
