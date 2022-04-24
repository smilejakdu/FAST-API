from fastapi import APIRouter


router = APIRouter(
    prefix="/bOARD",
    tags=["BOARD"]
)

@router.get("/find_board",status_code = 200)
async def find_board(board_id:int):
    return 

@router.post("",status_code=201)
async def create_board():
    return


@router.get("{board_id}",response_model=CoreResponse, status_code=200)
async def update_board(body:BoardDto,board_id:int):
    return
