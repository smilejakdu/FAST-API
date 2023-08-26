import pytest


@pytest.mark.asyncio
async def test_create_user_success(client, mocker):
    mocker.patch("services.user_service.get_user_by_email", return_value=None)
    body = {
        "id": 1,
        "email": "ash@gmail.com",
        "nickname": "ash",
        "password": "1234"
    }
    mocker.patch("api.user.create_user", return_value=body)
    mocker.patch("api.user.create_access_token", return_value="sample_access_token")

    response = client.post("/user/sign_up", json=body)
    assert response.status_code == 201
    assert response.json() == {
            "ok": True,
            "status_code": 201,
            "message": "User created successfully"
    }
