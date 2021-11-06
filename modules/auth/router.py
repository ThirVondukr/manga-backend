from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordRequestFormStrict
from pydantic import SecretStr

from modules.auth.services import AuthService
from . import exceptions, schema
from ..users.repositories import UserRepository

auth_router = APIRouter()


@auth_router.post(
    "/token/",
    response_model=schema.TokenSchema,
)
async def login(
    form_data: OAuth2PasswordRequestFormStrict = Depends(),
    user_repository: UserRepository = Depends(),
    auth_service: AuthService = Depends(),
) -> schema.TokenSchema:
    user = await user_repository.get_by_username(username=form_data.username)
    if user is None:
        raise exceptions.InvalidCredentialsError

    if not await auth_service.verify_user_password(user=user, password=form_data.password):
        raise exceptions.InvalidCredentialsError

    return auth_service.create_token(user)


@auth_router.post(
    "/token/validate/",
    response_model=bool,
)
async def validate_token(
    token: SecretStr = Body(..., embed=True),
    auth_service: AuthService = Depends(),
):
    return await auth_service.validate_jwt(token.get_secret_value())
