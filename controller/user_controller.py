from fastapi import APIRouter, Depends

from controller.dto.user_controller_dto.user_request_dto import CreateRequestDto, UpdateRequestDto, LoginRequestDto
from controller.dto.user_controller_dto.user_response_dto import LoginResponse, MyInfoResponse, UpdateUserResponse
from repository.user_repository import UserRepository
from services import user_service
from services.user_service import get_user_from_token
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
async def create_user(
    body: CreateRequestDto,
    user_repo: UserRepository = Depends(UserRepository)
):
    return await user_service.create_user(body, user_repo)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=200,
    summary="로그인",
    description="로그인하고 cookie token 을 받는다."
)
async def login_user(
    body: LoginRequestDto,
    user_repo: UserRepository = Depends(UserRepository)
):
    return await user_service.login_user(body, user_repo)


@router.get(
    "/my_info",
    response_model=MyInfoResponse,
    status_code=200,
    summary="내 정보",
    description="내 정보를 가져온다."
)
async def my_info(
    user: dict = Depends(get_user_from_token)
):
    return await user_service.my_info(user)


@router.put(
    "",
    response_model=UpdateUserResponse,
    status_code=200,
    summary="수정하고 나서 내정보를 가져온다.",
    description="수정하고 나서 내정보를 가져온다."
)
async def update_user(
    body: UpdateRequestDto,
    user_repo: UserRepository = Depends(UserRepository),
    user: dict = Depends(get_user_from_token),
):
    return await user_service.update_user(
        body,
        user_repo,
        user
    )
