from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    class Config:
        env_prefix = "db_"

    driver: str
    database: str
    username: str
    password: str
    host: str

    echo: bool

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.username}:{self.password}@{self.host}/{self.database}"


class AuthSettings(BaseSettings):
    class Config:
        env_prefix = "auth_"

    secret_key: str
    algorithm: str
    token_lifetime_min: int


database = DatabaseSettings(_env_file=".env")
auth = AuthSettings(_env_file=".env")
