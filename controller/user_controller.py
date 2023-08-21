from fastapi import APIRouter, Request, HTTPException

from controller.dto.user_controller_dto.user_request_dto import CreateRequestDto, UpdateRequestDto, LoginRequestDto
from controller.dto.user_controller_dto.user_response_dto import LoginResponse, MyInfoResponse
from services.user_service import UserService
from shared.core_response import CoreResponse

ACCESS_TOKEN_COOKIE = "access-token"

router = APIRouter(
    prefix="/user",
    tags=["USER"],
)


async def get_access_token(request: Request) -> str:
    access_token = request.cookies.get(ACCESS_TOKEN_COOKIE)
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return access_token


@router.post(
    "/sign_up",
    response_model=CoreResponse,
    status_code=201,
    summary="회원가입",
    description="회원가입을 한다."
)
async def create_user(body: CreateRequestDto):
    return await UserService.create_user(body)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=200,
    summary="로그인",
    description="로그인하고 cookie token 을 받는다."
)
async def login_user(
    login_request_dto: LoginRequestDto
):
    return await UserService.login_user(login_request_dto)


@router.get(
    "/my_info",
    response_model=MyInfoResponse,
    status_code=200,
    summary="내 정보",
    description="내 정보를 가져온다."
)
async def my_info(request: Request):
    access_token = request.cookies.get(ACCESS_TOKEN_COOKIE)
    return await UserService.my_info(access_token)


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
):
    access_token = request.cookies.get("access-token")
    return await UserService.update_user(body, access_token)
