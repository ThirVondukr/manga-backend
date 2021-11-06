from datetime import datetime, timedelta

from fastapi import Depends
from jose import jwt
from passlib.context import CryptContext

from db.dependencies import get_session_dependency
from db.models.users import User
from settings import auth
from . import schema


class AuthService:
    def __init__(self, session = Depends(get_session_dependency)):
        self.session = session
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
            token_type="bearer"
        )
