import pytest
from fastapi import status
from httpx import Response

from db.models.users import User


@pytest.fixture
async def auth_response(
    http_client,
    user_in_db: User,
    user_in_db_password,
) -> Response:
    body = {
        "grant_type": "password",
        "username": user_in_db.username,
        "password": user_in_db_password,
    }
    return await http_client.post("/api/auth/token/", data=body)


@pytest.mark.asyncio
async def test_can_authenticate(
    auth_response: Response,
):
    assert auth_response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_can_validate_token(
    http_client,
    auth_response: Response,
):
    token = auth_response.json()["accessToken"]
    body = {"token": token}
    response = await http_client.post("/api/auth/token/validate/", json=body)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is True
