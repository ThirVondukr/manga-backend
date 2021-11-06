from datetime import datetime, timedelta
from uuid import UUID

from fastapi import Depends
from jose import jwt, JWTError
from passlib.context import CryptContext

from db.dependencies import get_session_dependency
from db.models.users import User
from settings import auth
from . import exceptions, schema
from ..users.repositories import UserRepository


class AuthService:
    def __init__(
        self,
        session=Depends(get_session_dependency),
        user_repository: UserRepository = Depends(),
    ):
        self.session = session
        self.user_repository = user_repository
        self.context = CryptContext(
            schemes=["argon2"],
        )

    async def verify_user_password(self, user: User, password: str) -> bool:
        is_valid, new_hash = self.context.verify_and_update(password, user.password_hash)

        if new_hash is not None:
            user.password_hash = new_hash
            self.session.add(user)
            await self.session.commit()

        return is_valid

    def update_user_password(self, user: User, password: str) -> None:
        user.password_hash = self.context.hash(password)

    def create_token(self, user: User) -> schema.TokenSchema:
        expires_at = datetime.utcnow() + timedelta(minutes=auth.token_lifetime_min)
        claims = {
            "sub": str(user.id),
            "exp": expires_at,
        }
        token = jwt.encode(claims, key=auth.secret_key, algorithm=auth.algorithm)

        return schema.TokenSchema(
            access_token=token,
            token_type="bearer",
        )

    async def get_user_from_jwt(self, token: str) -> User:
        try:
            payload = jwt.decode(token, auth.secret_key, algorithms=[auth.algorithm])
        except JWTError:
            raise exceptions.InvalidCredentialsError
        user_id = payload.get("sub")
        if user_id is None:
            raise exceptions.InvalidCredentialsError

        user = await self.user_repository.get(UUID(user_id))
        if user is None:
            raise exceptions.InvalidCredentialsError

        return user

    async def validate_jwt(self, token: str) -> bool:
        try:
            await self.get_user_from_jwt(token)
        except exceptions.InvalidCredentialsError:
            return False
        return True
