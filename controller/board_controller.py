from fastapi import APIRouter

from controller.dto.BoardControllerDto.BoardRequestDto import BoardDto
from shared.core_response import CoreResponse

router = APIRouter(
    prefix="/board",
    tags=["BOARD"]
)


@router.get("/find_board", status_code=200)
async def find_board(board_id: int):
    return


@router.post("", response_model=CoreResponse, status_code=201)
async def create_board(body: BoardDto):
    print(body)
    return


@router.get("{board_id}", response_model=CoreResponse, status_code=200)
async def update_board(body: BoardDto, board_id: int):
    return