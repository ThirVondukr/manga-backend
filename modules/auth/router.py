from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestFormStrict
from jose import jwt
from sqlalchemy.exc import NoResultFound

from db.models.users import User
from modules.auth.services import HashingService
from modules.users.services import UserService
from settings import auth
from . import exceptions, schema

auth_router = APIRouter()


def create_token(user: User) -> str:
    expires_at = datetime.utcnow() + timedelta(minutes=auth.token_lifetime_min)
    claims = {
        "sub": str(user.id),
        "exp": expires_at,
    }
    token = jwt.encode(claims, key=auth.secret_key, algorithm=auth.algorithm)
    return token


@auth_router.post(
    "/token/",
    response_model=schema.TokenSchema,
)
async def login(
    form_data: OAuth2PasswordRequestFormStrict = Depends(),
    user_service: UserService = Depends(),
    hash_service: HashingService = Depends(),
) -> schema.TokenSchema:
    user = await user_service.get_by_username(username=form_data.username)
    if user is None:
        raise exceptions.InvalidCredentialsError

    if not hash_service.verify(form_data.password, user.password_hash):
        raise exceptions.InvalidCredentialsError

    return schema.TokenSchema(
        access_token=create_token(user),
        token_type="bearer",
    )
