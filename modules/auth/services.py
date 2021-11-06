from passlib.context import CryptContext

from db.models.users import User


class HashingService:
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
