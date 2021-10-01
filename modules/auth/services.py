from passlib.context import CryptContext


class HashingService:
    def __init__(self):
        self.context = CryptContext(schemes=["argon2"])

    def hash(self, secret: str) -> str:
        return self.context.hash(secret)

    def verify(self, secret: str, hash_: str) -> bool:
        return self.context.verify(secret, hash_)
