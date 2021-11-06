from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies import get_session_dependency
from db.models.users import User
from modules.auth.services import AuthService
from . import exceptions
from .repositories import UserRepository
from .schema import UserCreateSchema


class UserService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session_dependency),
        auth_service: AuthService = Depends(),
        user_repository: UserRepository = Depends(),
    ):
        self.session = session
        self.auth_service = auth_service
        self.user_repository = user_repository

    async def _create(self, user_model: UserCreateSchema) -> User:
        user = User(
            username=user_model.username,
            email=user_model.email,
        )
        self.auth_service.update_user_password(
            user=user,
            password=user_model.password.get_secret_value(),
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def create(self, user_model: UserCreateSchema) -> User:
        duplicate_username = await self.user_repository.get_by_username(username=user_model.username)
        if duplicate_username:
            raise exceptions.UsernameIsTakenError

        duplicate_email = await self.user_repository.get_by_clause(User.email == user_model.email)
        if duplicate_email:
            raise exceptions.EmailIsTakenError

        user = await self._create(user_model)
        return user
