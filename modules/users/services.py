from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies import get_session_dependency
from db.models import users
from db.models.users import User
from modules.auth.services import HashingService
from . import exceptions
from .schema import UserCreateSchema


class UserService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session_dependency),
        hash_service: HashingService = Depends(),
    ):
        self._session = session
        self._hash_service = hash_service

    async def _get_user(self, clause) -> Optional[User]:
        query = select(User).filter(clause)
        return (await self._session.execute(query)).scalar_one_or_none()

    async def get(self, user_id: UUID) -> User:
        stmt = select(User).filter(User.id == user_id)
        result = await self._session.execute(stmt)
        user: users.User = result.scalar_one()
        return user

    async def get_by_username(self, username: str) -> Optional[User]:
        return await self._get_user(User.username == username)

    async def _create(self, user_model: UserCreateSchema) -> User:
        user = User(
            username=user_model.username,
            email=user_model.email,
        )
        self._hash_service.update_user_password(
            user=user,
            password=user_model.password.get_secret_value()
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def create(self, user_model: UserCreateSchema) -> User:
        duplicate_username = await self._get_user(User.username == user_model.username)
        if duplicate_username:
            raise exceptions.UsernameIsTakenError

        duplicate_email = await self._get_user(User.email == user_model.email)
        if duplicate_email:
            raise exceptions.EmailIsTakenError

        user = await self._create(user_model)
        return user
