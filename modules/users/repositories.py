from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies import get_session_dependency
from db.models.users import User


class UserRepository:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session_dependency),
    ):
        self.session = session

    async def get(self, user_id: UUID) -> Optional[User]:
        query = select(User).filter(User.id == user_id)
        return (await self.session.scalars(query)).one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        query = select(User).filter(User.username == username)
        return (await self.session.scalars(query)).one_or_none()

    async def get_by_clause(self, clause) -> Optional[User]:
        query = select(User).filter(clause)
        return (await self.session.scalars(query)).one_or_none()
