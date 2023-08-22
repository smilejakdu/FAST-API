def test_health_check_handler(client):
    response = client.get("/health")
    assert response.status_code == 200  # true 인지 false 인지 확인
    assert response.json() == "health check ok"

