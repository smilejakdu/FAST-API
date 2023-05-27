from http import HTTPStatus
from typing import Optional

import sqlalchemy
from fastapi import HTTPException
from jwt import decode
from requests import Session
from starlette.responses import JSONResponse

from controller.dto.board_controller_dto.board_request_dto import BoardDto, QueryFindBoardRequestDto
from my_settings import ALGORITHM, SECRET_KEY
from repository import user_repository, board_repository


def to_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in sqlalchemy.inspect(obj).mapper.column_attrs}


def tuple_to_dict(tup):
    board_dict = to_dict(tup[0])
    board_dict["email"] = tup[1]
    return board_dict


async def find_board_all(
        db: Session,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        search: Optional[str] = None,
):
    response_find_board = await board_repository.find_board_by_search(
        db,
        page,
        page_size,
        search,
    )
    if not response_find_board:
        raise HTTPException(status_code=404, detail="게시판 글이 존재하지 않습니다.")

    response_find_board = [tuple_to_dict(tup) for tup in response_find_board]

    try:
        return {
            'ok': True,
            'status_code': HTTPStatus.OK,
            'message': '게시판 데이터',
            'data': response_find_board,
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Bad Request")


async def create_board(db: Session, body: BoardDto, access_token: str):
    if not body:
        raise HTTPException(status_code=400, detail="값을 입력해주세요")

    try:
        payload = decode(
            access_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        email_from_token = payload.get("sub")
        user_info = user_repository.find_user_by_email(db, email_from_token)
        if not user_info:
            raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")

        response_created_board = await board_repository.create_board(
            db,
            body,
            user_info["id"],
        )
        print('response_created_board:', response_created_board)

        return JSONResponse({
            "ok": True,
            "status_code": HTTPStatus.OK,
            "message": "Board Successful",
            "data": dict(response_created_board),
        })
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Bad Request")
