from uuid import UUID

from pydantic import EmailStr, SecretStr, constr, Field

from app.schema import SchemaBase


class UserCreateSchema(SchemaBase):
    class Config:
        title = "CreateUser"

    username: constr(min_length=5, max_length=24)
    email: EmailStr
    password: SecretStr = Field(min_length=8, max_length=48)


class UserSchema(SchemaBase):
    class Config:
        title = "User"

    id: UUID
    username: str
    email: EmailStr
    avatar_url: str
