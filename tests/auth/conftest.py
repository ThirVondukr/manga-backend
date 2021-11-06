import pytest

from db.models.users import User
from modules.auth.services import AuthService


@pytest.fixture(scope="module")
def auth_service() -> AuthService:
    return AuthService()


@pytest.fixture
def user_in_db_password() -> str:
    return "password"


@pytest.fixture
async def user_in_db(session, user_in_db_password, auth_service) -> User:
    user = User(
        username="Username",
        email="example@test.com",
    )
    auth_service.update_user_password(user, user_in_db_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
