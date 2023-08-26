from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from controller.dto.board_controller_dto.board_request_dto import BoardDto, \
    FindBoardRequestDto
from controller.dto.board_controller_dto.board_response_dto import ResponseFindBoardAll, \
    CreateResponseBoard
from models.connection import get_db
from repository.board_repository import BoardRepository
from services import board_service
from services.user_service import get_user_from_token

router = APIRouter(
    prefix="/board",
    tags=["BOARD"]
)


@router.get(
    "",
    response_model=ResponseFindBoardAll,
    status_code=200,
    summary="전체 게시판 불러오기",
    description="전체 게시판 불러오기"
)
async def find_board_all(
    query: FindBoardRequestDto = Depends(),
    db: Session = Depends(get_db),
):
    page, page_size, search = query.page, query.page_size, query.search
    return await board_service.find_board_all(
        db,
        page,
        page_size,
        search,
    )


@router.get(
    "/my_board",
    response_model=ResponseFindBoardAll,
    status_code=200,
    summary="내가 작성한 게시판 가져오기",
    description="내가 작성한 게시판 가져오기"
)
async def find_my_board(
    find_board_request: FindBoardRequestDto = Depends(),
    user: dict = Depends(get_user_from_token),
    board_repo: BoardRepository = Depends(BoardRepository),
):
    page = find_board_request.page
    page_size = find_board_request.page_size
    search = find_board_request.search

    return await board_service.find_my_board(
        board_repo,
        user,
        page,
        page_size,
        search
    )


@router.get(
    "/{board_id}",
    status_code=200,
    summary="게시판 상세보기",
    description="게시판 상세보기"
)
async def find_board_by_id(
    request: Request,
    board_id: int,
    db: Session = Depends(get_db),
):
    return await board_service.find_board_by_id(db, board_id)


@router.put(
    "/{board_id}",
    status_code=200,
    summary="게시판 수정",
    description="게시판을 수정 한다."
)
async def update_board(
    board_id: int,
    body: BoardDto,
    user: dict = Depends(get_user_from_token),
    board_repo: BoardRepository = Depends(BoardRepository)
):
    return await board_service.update_board(
        board_id,
        body,
        user,
        board_repo
    )


@router.delete(
    "/{board_id}",
    status_code=200,
    summary="게시판 삭제",
    description="게시판을 삭제 한다."
)
async def delete_board(request: Request, board_id: int, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access-token")
    return await board_service.delete_board(db, board_id, access_token)


@router.post(
    "",
    response_model=CreateResponseBoard,
    status_code=201,
    summary="게시판 생성",
    description="게시판을 생성 한다."
)
async def create_board(
    body: BoardDto,
    user: dict = Depends(get_user_from_token),
    board_repo: BoardRepository = Depends(BoardRepository)
):
    return await board_service.create_board(
        user,
        body,
        board_repo
    )
