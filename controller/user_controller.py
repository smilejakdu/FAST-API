from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from controller.dto.UserControllerDto.UserRequestDto import CreateRequestDto, UpdateRequestDto, LoginRequestDto
from models.connection import get_db
from my_settings import SECRET_KEY, ALGORITHM
from services import user_service
from shared.core_response import CoreResponse, LoginResponse

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/find_user_all", status_code=200)
def find_user(db: Session = Depends(get_db)):
    return user_service.find_user_all(db)


@router.post("/sign_up", response_model=CoreResponse, status_code=201)
async def create_user(body: CreateRequestDto, db: Session = Depends(get_db)):
    return await user_service.create_user(body, db)


@router.post("/login", response_model=LoginResponse, status_code=200)
async def login_user(body: LoginRequestDto, db: Session = Depends(get_db)):
    return await user_service.login_user(body, db)


@router.get("/my_info", response_model=LoginResponse, status_code=200)
async def my_info(request: Request, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access-token")
    return await user_service.my_info(db, access_token)


@router.get("/{user_id}", status_code=200)
async def find_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.find_user_by_id(db, user_id)


@router.put("/{user_id}", response_model=CoreResponse, status_code=200)
async def update_user(body: UpdateRequestDto, user_id: int):
    return user_service.update_user(user_id, body)
