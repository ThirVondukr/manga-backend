from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestFormStrict

from modules.auth.services import AuthService
from modules.users.services import UserService
from . import exceptions, schema

auth_router = APIRouter()


@auth_router.post(
    "/token/",
    response_model=schema.TokenSchema,
)
async def login(
    form_data: OAuth2PasswordRequestFormStrict = Depends(),
    user_service: UserService = Depends(),
    auth_service: AuthService = Depends(),
) -> schema.TokenSchema:
    user = await user_service.get_by_username(username=form_data.username)
    if user is None:
        raise exceptions.InvalidCredentialsError

    if not auth_service.verify_user_password(user=user, password=form_data.password):
        raise exceptions.InvalidCredentialsError

    return auth_service.create_token(user)
