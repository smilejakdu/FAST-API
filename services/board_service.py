from http import HTTPStatus

from fastapi import HTTPException
from jwt import decode
from requests import Session
from starlette.responses import JSONResponse

from controller.dto.board_controller_dto.board_request_dto import BoardDto
from my_settings import ALGORITHM, SECRET_KEY
from repository import user_repository, board_repository


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
