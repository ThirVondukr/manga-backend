from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    class Config:
        env_file = "env/database.env"

    database_url: str
    echo: bool


database_settings = DatabaseSettings()
