from typing import Optional
from uuid import UUID

from sqlalchemy import select

from db.dependencies import get_session
from db.models.users import User
from gql.context import Info
from gql.users.types import UserType


async def get_viewer(info: Info) -> Optional[UserType]:
    user = await info.context.user()
    return UserType.maybe_from_orm(user)


async def get_user_by_id(user_id: UUID) -> Optional[UserType]:
    query = select(User).filter(User.id == user_id).limit(1)
    async with get_session() as session:
        user: Optional[User] = (await session.execute(query)).scalar_one_or_none()

    return UserType.maybe_from_orm(user)


async def get_user_by_username(username: str) -> Optional[UserType]:
    query = select(User).filter(User.username == username).limit(1)
    async with get_session() as session:
        user: Optional[User] = (await session.execute(query)).scalar_one_or_none()

    return UserType.maybe_from_orm(user)
