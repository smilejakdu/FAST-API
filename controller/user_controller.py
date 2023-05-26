from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from controller.dto.UserControllerDto.UserRequestDto import CreateRequestDto, UpdateRequestDto, LoginRequestDto
from models.connection import get_db
from my_settings import SECRET_KEY, ALGORITHM
from services import user_service
from shared.core_response import CoreResponse, LoginResponse, MyInfoResponse

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post(
    "/sign_up",
    response_model=CoreResponse,
    status_code=201,
    summary="회원가입",
    description="회원가입을 한다."
)
async def create_user(body: CreateRequestDto, db: Session = Depends(get_db)):
    return await user_service.create_user(body, db)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=200,
    summary="로그인",
    description="로그인하고 cookie token 을 받는다."
)
async def login_user(body: LoginRequestDto, db: Session = Depends(get_db)):
    return await user_service.login_user(body, db)


@router.get(
    "/my_info",
    response_model=MyInfoResponse,
    status_code=200,
    summary="내 정보",
    description="내 정보를 가져온다."
)
async def my_info(request: Request, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access-token")
    return await user_service.my_info(db, access_token)


@router.put("/{user_id}", response_model=CoreResponse, status_code=200)
async def update_user(body: UpdateRequestDto, user_id: int):
    return user_service.update_user(user_id, body)
