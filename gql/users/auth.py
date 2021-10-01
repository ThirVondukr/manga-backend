from typing import Optional

from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.engine import Result
from starlette.requests import Request
from strawberry.types import Info

from db.dependencies import get_session
from db.models.users import User
from modules.auth import settings as auth_settings

_CURRENT_USER_KEY = "Auth_CurrentUser"

MaybeUser = Optional[User]


def get_user(info: Info) -> MaybeUser:
    return info.context[_CURRENT_USER_KEY]


def put_user_into_context(ctx: dict, user: MaybeUser):
    ctx[_CURRENT_USER_KEY] = user


async def get_user_from_request(request: Request) -> MaybeUser:
    if "Authorization" not in request.headers:
        return None

    token = request.headers["Authorization"].replace("Bearer ", "", 1)

    try:
        payload = jwt.decode(
            token, auth_settings.secret_key, algorithms=[auth_settings.algorithm]
        )
        user_id = payload.get("sub", None)
        async with get_session() as session:
            result: Result = await session.execute(
                select(User).filter(User.id == user_id).limit(1)
            )
        user = result.scalar_one_or_none()
        return user
    except JWTError:
        return None
