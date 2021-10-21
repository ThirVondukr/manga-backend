from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestFormStrict
from jose import jwt
from sqlalchemy.exc import NoResultFound

from db.models.users import User
from modules.auth.services import HashingService
from modules.users.services import UserService
from settings import settings

auth_router = APIRouter()


def create_token(user: User) -> str:
    expires_at = datetime.utcnow() + timedelta(minutes=settings.token_lifetime_min)
    claims = {
        "sub": str(user.id),
        "exp": expires_at,
    }
    token = jwt.encode(claims, key=settings.secret_key, algorithm=settings.algorithm)
    return token


@auth_router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestFormStrict = Depends(),
    user_service: UserService = Depends(),
    hash_service: HashingService = Depends(),
):
    exception = HTTPException(status_code=400, detail="Incorrect username or password.")
    try:
        user = await user_service.get_by_username(username=form_data.username)
    except NoResultFound:
        raise exception

    if not hash_service.verify(form_data.password, user.password_hash):
        raise exception

    return {"access_token": create_token(user), "token_type": "bearer"}
