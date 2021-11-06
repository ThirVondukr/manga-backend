from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from db.models.users import User
from settings import auth
from . import schema


class AuthService:
    def __init__(self):
        self.context = CryptContext(
            schemes=["argon2"],
        )

    def verify_user_password(self, user: User, password: str) -> bool:
        return self.context.verify(
            password,
            user.password_hash,
        )

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
