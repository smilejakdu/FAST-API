from starlette import status

from models.user_entity import user_entity
from repository import user_repository


async def test_health_check_handler(client):
    response = client.get("/health")
    assert response.status_code == 200  # true 인지 false 인지 확인
    assert response.json() == "health check ok"

