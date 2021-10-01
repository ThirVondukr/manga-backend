from uuid import UUID

from pydantic import EmailStr, SecretStr

from app.schema import SchemaBase


class _UserSchemaBase(SchemaBase):
    username: str
    email: EmailStr


class CreateUserSchema(_UserSchemaBase):
    class Config:
        title = "CreateUser"

    password: SecretStr


class UserSchema(_UserSchemaBase):
    class Config:
        title = "User"

    id: UUID
    avatar_url: str
