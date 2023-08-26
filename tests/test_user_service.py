from unittest.mock import AsyncMock

import pytest

from controller.dto.user_controller_dto.user_request_dto import CreateRequestDto
from repository.user_repository import UserRepository


@pytest.mark.asyncio
async def test_create_user_success(client, mocker):
    # 임의의 요청 바디 생성
    body = CreateRequestDto(
        email="test@test.com",
        nickname="test",
        password="test1234",
    )

    # UserRepository의 mock 객체 생성
    user_repo = AsyncMock(spec=UserRepository)
    # find_user_by_email 메서드가 None을 반환하도록 설정 (즉, 이메일이 중복되지 않음을 의미)
    user_repo.find_user_by_email.return_value = None

    # 비밀번호 암호화 및 user_entity.create 함수 mock 처리
    with mocker.patch.object(
        "services.user_service",
        "hash_password",
        return_value="encrypted_password".encode('utf-8')
    ), \
        mocker.patch.object(
            "models.user_entity.user_entity.create",
            return_value=None
        ):
        # 함수 실행
        response = client.post("/user/sign_up", json=body)

    # 반환 값 확인
    assert response.status_code == 201
    assert response == {
        "ok": True,
        "status_code": 201,
        "message": "User created successfully."
    }
