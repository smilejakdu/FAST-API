from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from controller.dto.user_controller_dto.user_request_dto import CreateRequestDto, UpdateRequestDto, LoginRequestDto
from controller.dto.user_controller_dto.user_response_dto import LoginResponse, MyInfoResponse
from models.connection import get_db
from services import user_service
from shared.core_response import CoreResponse

router = APIRouter(
    prefix="/user",
    tags=["USER"],
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


@router.put(
    "",
    response_model=MyInfoResponse,
    status_code=200,
    summary="수정하고 나서 내정보를 가져온다.",
    description="수정하고 나서 내정보를 가져온다."
)
async def update_user(
        request: Request,
        body: UpdateRequestDto,
        db: Session = Depends(get_db),
):
    access_token = request.cookies.get("access-token")
    print('access_token:', access_token)
    return await user_service.update_user(db, body, access_token)
