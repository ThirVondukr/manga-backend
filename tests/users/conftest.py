import httpx
import pytest


@pytest.fixture
async def create_user_response(http_client) -> httpx.Response:
    body = {
        "username": "username",
        "password": "password",
        "email": "test@example.com",
    }
    response = await http_client.post("/api/users", json=body)
    return response
