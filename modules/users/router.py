from fastapi import APIRouter, Depends, status

from db.models.users import User
from modules.auth.dependencies import current_user
from . import schema
from .services import UserService

users_router = APIRouter()


@users_router.get(
    "/me/",
    response_model=schema.UserSchema,
)
async def me(user: User = Depends(current_user)):
    return user


@users_router.post(
    "/",
    response_model=schema.UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: schema.CreateUserSchema,
    user_service: UserService = Depends(),
):
    return await user_service.create(user_model=user)
