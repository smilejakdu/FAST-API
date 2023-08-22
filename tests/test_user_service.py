from starlette import status

from models.user_entity import user_entity
from repository import user_repository


def test_create_user(client):
    response = client.post(
        "/user/sign_up",
        json={
            "email": "ash@gmail.com",
            "password": "1234",
            "nickname": "test"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
