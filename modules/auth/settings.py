from pydantic import BaseSettings


class AuthSettings(BaseSettings):
    class Config:
        env_file = "env/auth.env"

    secret_key: str
    algorithm: str
    token_lifetime_min: int


settings = AuthSettings()
