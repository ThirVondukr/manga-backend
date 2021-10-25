from typing import Literal

from app.schema import SchemaBase


class TokenSchema(SchemaBase):
    class Config:
        title = "Token"

    access_token: str
    token_type: Literal["bearer"]
