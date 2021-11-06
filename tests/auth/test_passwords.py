import contextlib
from typing import Callable, ContextManager

import hypothesis
import pytest
from hypothesis.strategies import text

from db.models.users import User


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


@hypothesis.given(password=text())
@pytest.mark.asyncio
@pytest.mark.slow
async def test_can_verify_hashed_password(auth_service, get_user, password):
    with get_user() as user:
        auth_service.update_user_password(user, password)
        assert await auth_service.verify_user_password(user, password)


@hypothesis.given(password=text(), another_password=text())
@pytest.mark.asyncio
@pytest.mark.slow
async def test_cant_verify_another_password(
    auth_service,
    get_user,
    password: str,
    another_password: str,
):
    hypothesis.assume(password != another_password)

    with get_user() as user:
        auth_service.update_user_password(user, password)
        assert not await auth_service.verify_user_password(user, another_password)
