import pytest


@pytest.mark.asyncio
async def test_create_user_success(client, mocker):
    hash_password = mocker.patch.object(
        useer_service,
        "hash_password",
        return_value="hashed",
    )
