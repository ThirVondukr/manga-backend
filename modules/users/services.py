from typing import Sequence
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies import get_session_dependency
from db.models import users
from db.models.users import User
from modules.auth.services import HashingService
from .schema import CreateUserSchema


class UserService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session_dependency),
        hash_service: HashingService = Depends(),
    ):
        self._session = session
        self._hash_service = hash_service

    async def get(self, user_id: UUID) -> users.User:
        stmt = select(User).filter(User.id == user_id)
        result = await self._session.execute(stmt)
        user: users.User = result.scalar_one()
        return user

    async def get_by_username(self, username: str) -> users.User:
        stmt = select(User).filter(User.username == username)
        return (await self._session.execute(stmt)).scalar_one()

    async def list(self, username: str) -> Sequence[users.User]:
        stmt = select(User)
        if username:
            stmt = stmt.filter(User.username == username)
        result: Result = await self._session.execute(stmt)
        return result.scalars().all()

    async def create(self, user_model: CreateUserSchema) -> users.User:
        user = User(
            username=user_model.username,
            email=user_model.email,
            password_hash=self._hash_service.hash(user_model.password.get_secret_value()),
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def delete(self, user: User):
        await self._session.delete(user)
        await self._session.commit()
