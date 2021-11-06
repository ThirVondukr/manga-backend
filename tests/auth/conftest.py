import contextlib
from typing import ContextManager, Callable

import pytest

from db.models.users import User
from modules.auth.services import HashingService


@pytest.fixture(scope="module")
def hash_service() -> HashingService:
    return HashingService()


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
