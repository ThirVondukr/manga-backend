from pydantic import BaseSettings


class AuthSettings(BaseSettings):
    class Config:
        env_prefix = "auth_"

    secret_key: str
    algorithm: str
    token_lifetime_min: int


settings = AuthSettings()
