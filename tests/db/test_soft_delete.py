import pytest
from sqlalchemy import select

from db.models.users import User


@pytest.fixture
async def user(session) -> User:
    user = User(
        username="username",
        password_hash="",
        email="test@example.com",
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.fixture
async def deleted_user(user: User, session) -> User:
    user.is_deleted = True
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.mark.asyncio
async def test_can_retrieve_row(user: User, session):
    row = await session.scalar(select(User).filter(User.id == user.id))
    assert row is not None


@pytest.mark.asyncio
async def test_cant_retrieve_row_if_deleted(deleted_user: User, session):
    row = await session.scalar(select(User).filter(User.id == deleted_user.id))
    assert row is None


@pytest.mark.asyncio
async def test_can_retrieve_deleted_row_if_execution_option_is_passed(deleted_user: User, session):
    row = await session.scalar(
        select(User)
        .filter(User.id == deleted_user.id)
        .execution_options(include_deleted=True)
    )
    assert row is not None
    assert isinstance(row, User)
