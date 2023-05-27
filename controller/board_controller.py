from typing import Optional

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from controller.dto.board_controller_dto.board_request_dto import BoardDto
from controller.dto.board_controller_dto.board_response_dto import ResponseCreateBoard
from models.connection import get_db
from services import board_service
from shared.core_response import CoreResponse

router = APIRouter(
    prefix="/board",
    tags=["BOARD"]
)


@router.get(
    "",
    status_code=200,
    summary="게시판 불러오기",
    description="게시판 불러오기"
)
async def find_board(q: Optional[str] = None, db: Session = Depends(get_db)):
    if q:
        return {"items": "results for " + q}
    return


@router.post(
    "",
    response_model=ResponseCreateBoard,
    status_code=201,
    summary="게시판생성",
    description="게시판을 생성 한다."
)
async def create_board(request: Request, body: BoardDto, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access-token")
    return await board_service.create_board(db, body, access_token)


@router.get("{board_id}", response_model=CoreResponse, status_code=200)
async def update_board(body: BoardDto, board_id: int):
    return
