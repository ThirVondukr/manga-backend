from passlib.context import CryptContext

import settings


class HashingService:
    def __init__(self):
        self.context = CryptContext(
            schemes=["argon2"],
            argon2__type=settings.auth.argon2_type,
            argon2__rounds=settings.auth.argon2_rounds,
            argon2__memory_cost=settings.auth.argon2_memory_cost,
        )

    def hash(self, secret: str) -> str:
        return self.context.hash(secret)

    def verify(self, secret: str, hash_: str) -> bool:
        return self.context.verify(secret, hash_)
