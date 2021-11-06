import contextlib
from typing import ContextManager, Callable

import pytest

from db.models.users import User
from modules.auth.services import AuthService


@pytest.fixture(scope="module")
def auth_service() -> AuthService:
    return AuthService()


@pytest.fixture(scope="module")
def get_user() -> Callable[..., ContextManager[User]]:
    user = User(
        username="Username",
        email="example@text.com",
    )

    @contextlib.contextmanager
    def wrapper():
        yield user
        user.password_hash = None

    return wrapper
