from http import HTTPStatus
from typing import Optional

import sqlalchemy
from fastapi import HTTPException
from jwt import decode
from requests import Session
from starlette.responses import JSONResponse

from controller.dto.board_controller_dto.board_request_dto import BoardDto
from models import board_entity
from my_settings import ALGORITHM, SECRET_KEY
from repository import user_repository, board_repository
from shared.login_check import login_check
from shared.trans_mapper import to_dict


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
    try:
        response_find_board = await board_repository.find_board_by_search(
            db,
            page,
            page_size,
            search,
        )
        if not response_find_board:
            raise HTTPException(status_code=404, detail="게시판 글이 존재하지 않습니다.")

        response_find_board = [tuple_to_dict(tup) for tup in response_find_board]

        return {
            'ok': True,
            'status_code': HTTPStatus.OK,
            'message': '게시판 데이터',
            'data': response_find_board,
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Bad Request")


async def find_my_board(
    db: Session,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    access_token: str = None,
    search: str = None,
):
    found_user = await login_check(db, access_token)
    if not found_user:
        raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")

    response_find_my_board = await board_repository.find_my_board(
        db,
        found_user['email'],
        page,
        page_size,
        search,
    )

    if not response_find_my_board:
        raise HTTPException(status_code=404, detail="게시판 글이 존재하지 않습니다.")

    data = [{
        'id': board.id,
        'title': board.title,
        'content': board.content,
        'user_id': board.user_id,
        'created_at': str(board.created_at),  # assuming this is a datetime object
        'updated_at': str(board.updated_at),  # assuming this is a datetime object
        'deleted_at': str(board.deleted_at) if board.deleted_at else None,  # handle if datetime or None
    } for board in response_find_my_board]

    return JSONResponse({
        "ok": True,
        "status_code": HTTPStatus.OK,
        'message': '내 게시판 데이터',
        "data": data,
    })


async def create_board(db: Session, body: BoardDto, access_token: str):
    if not body:
        raise HTTPException(status_code=400, detail="board 값을 입력해주세요")

    try:
        found_user = await login_check(db, access_token)
        if not found_user:
            raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")

        response_created_board = await board_repository.create_board(
            db,
            body,
            found_user["id"],
        )

        data = {
            'id': response_created_board.id,
            'title': response_created_board.title,
            'content': response_created_board.content,
            'email': found_user['email'],
            'user_id': response_created_board.user_id,
            'created_at': str(response_created_board.created_at),  # assuming this is a datetime object
            'updated_at': str(response_created_board.updated_at),  # assuming this is a datetime object
            'deleted_at': str(response_created_board.deleted_at) if response_created_board.deleted_at else None,
        }

        return JSONResponse({
            "ok": True,
            "status_code": HTTPStatus.OK,
            "message": "Board Successful",
            "data": data,
        })
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Bad Request")


async def update_board(db: Session, board_id: int, body: BoardDto, access_token: str):
    if board_id is None:
        raise HTTPException(status_code=404, detail="게시판 ID를 입력해주세요")

    if not body:
        raise HTTPException(status_code=400, detail="값을 입력해주세요")

    try:
        found_user = await login_check(db, access_token)

        if not found_user:
            raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")

        if body.title is None or body.content is None:
            raise HTTPException(status_code=404, detail="데이터를 입력해주세요")

        response_updated_board: board_entity = await board_repository.update_board(
            db,
            board_id,
            body,
            found_user["id"],
        )

        return JSONResponse({
            "ok": True,
            "status_code": HTTPStatus.OK,
            "message": "Board Update Successful",
            "data": response_updated_board,
        })
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Bad Request")


async def delete_board(db: Session, board_id: int, access_token: str):
    if board_id is None:
        raise HTTPException(status_code=404, detail="게시판 ID를 입력해주세요")
    try:
        found_user = await login_check(db, access_token)

        if not found_user:
            raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")

        response_updated_board: board_entity = await board_repository.delete_board(
            db,
            board_id,
            found_user["id"],
        )

        return JSONResponse({
            "ok": True,
            "status_code": HTTPStatus.OK,
            "message": "Board Delete Successful",
            "data": response_updated_board,
        })
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Bad Request")
