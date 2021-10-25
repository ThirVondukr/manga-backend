import pytest
from fastapi import status
from httpx import Response
from sqlalchemy import select

from db.models.users import User


@pytest.mark.asyncio
def test_create_user_returns_201_created(create_user_response: Response):
    assert create_user_response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_user_is_saved_in_database(create_user_response: Response, session):
    response_json = create_user_response.json()
    user = await session.scalar(select(User).filter(User.username == response_json["username"]))
    assert user is not None
    assert user.username == response_json["username"]
