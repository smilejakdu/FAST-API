from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException, status
from requests import Session
from starlette.responses import JSONResponse

from controller.dto.board_controller_dto.board_request_dto import BoardDto
from models import board_entity
from repository import board_repository
from repository.board_repository import BoardRepository
from shared.error_response import CustomException
from shared.login_check import login_check
from shared.trans_mapper import to_dict


def tuple_to_dict(tup):
    board_dict = to_dict(tup[0])
    board_dict["email"] = tup[1]
    return board_dict


async def find_board_by_id(
    board_id: int,
    board_repo: BoardRepository,
):
    board = await board_repo.find_board_by_id(board_id)
    return board


async def find_board_all(
    board_repo: BoardRepository,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    search: Optional[str] = None,
):
    try:
        response_find_board = await board_repo.find_board_by_search(
            page,
            page_size,
            search,
        )
        if not response_find_board:
            raise CustomException(status_code=status.HTTP_404_NOT_FOUND, message="게시판 글이 존재하지 않습니다.")

        response_find_board = [tuple_to_dict(tup) for tup in response_find_board]

        return {
            'ok': True,
            'status_code': status.OK,
            'message': '게시판 데이터',
            'data': response_find_board,
        }
    except Exception as e:
        print(e)
        raise CustomException(status_code=status.HTTP_400_BAD_REQUEST, message="Bad Request")


async def find_my_board(
    board_repo: BoardRepository,
    user: dict,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    search: str = None,
):
    response_find_my_board = await board_repo.find_my_board(
        user['email'],
        page,
        page_size,
        search,
    )

    if not response_find_my_board:
        raise CustomException(message="게시판 글이 존재하지 않습니다.", status_code=status.HTTP_404_NOT_FOUND)

    data = [{
        'id': board.id,
        'title': board.title,
        'content': board.content,
        'user_id': board.user_id,
        'review_count': review_count if review_count else 0,
        'created_at': str(board.created_at),  # assuming this is a datetime object
        'updated_at': str(board.updated_at),  # assuming this is a datetime object
        'deleted_at': str(board.deleted_at) if board.deleted_at else None,  # handle if datetime or None
    } for board, review_count in response_find_my_board]

    return JSONResponse({
        "ok": True,
        "status_code": 200,
        'message': '내 게시판 데이터',
        "data": data,
    })


async def create_board(
    user: dict,
    body: BoardDto,
    board_repo: BoardRepository,
) -> JSONResponse:
    if not body:
        raise CustomException(status_code=status.HTTP_400_BAD_REQUEST, message="board 값을 입력해주세요")

    try:
        response_created_board = await board_repo.create_board(
            body,
            user["id"],
        )

        data = {
            'id': response_created_board.id,
            'title': response_created_board.title,
            'content': response_created_board.content,
            'email': user['email'],
            'user_id': response_created_board.user_id,
            'created_at': str(response_created_board.created_at),  # assuming this is a datetime object
            'updated_at': str(response_created_board.updated_at),  # assuming this is a datetime object
            'deleted_at': str(response_created_board.deleted_at) if response_created_board.deleted_at else None,
        }

        return JSONResponse({
            "ok": True,
            "status_code": status.HTTP_201_CREATED,
            "message": "Board Successful",
            "data": data,
        })
    except Exception as e:
        print(e)
        raise CustomException(status_code=400, message="Bad Request")


async def update_board(
    board_id: int,
    body: BoardDto,
    user: dict,
    board_repo: BoardRepository,
):
    if board_id is None:
        raise CustomException(status_code=404, message="게시판 ID를 입력해주세요")

    if not body:
        raise CustomException(status_code=400, message="값을 입력해주세요")

    try:

        if not user:
            raise CustomException(status_code=404, message="존재하지 않는 유저입니다.")

        if body.title is None or body.content is None:
            raise CustomException(status_code=404, message="데이터를 입력해주세요")

        response_updated_board: board_entity = await board_repo.update_board(
            board_id,
            body,
            user["id"],
        )

        return JSONResponse({
            "ok": True,
            "status_code": HTTPStatus.OK,
            "message": "Board Update Successful",
            "data": response_updated_board,
        })
    except Exception as e:
        print(e)
        raise CustomException(status_code=400, message="Bad Request")


async def delete_board(
    board_repo: BoardRepository,
    board_id: int,
    user: dict,
):
    if board_id is None:
        raise CustomException(status_code=404, message="게시판 ID를 입력해주세요")
    try:
        if not user:
            raise CustomException(status_code=404, message="존재하지 않는 유저입니다.")

        response_updated_board: board_entity = await board_repo.delete_board(
            board_id,
            user["id"],
        )

        return JSONResponse({
            "ok": True,
            "status_code": HTTPStatus.OK,
            "message": "Board Delete Successful",
            "data": response_updated_board,
        })
    except Exception as e:
        print(e)
        raise CustomException(status_code=400, message="Bad Request")
