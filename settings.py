from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    class Config:
        env_prefix = "db_"

    database_url: str
    echo: bool


class AuthSettings(BaseSettings):
    class Config:
        env_prefix = "auth_"

    secret_key: str
    algorithm: str
    token_lifetime_min: int


database_settings = DatabaseSettings(_env_file=".env")
settings = AuthSettings(_env_file=".env")
