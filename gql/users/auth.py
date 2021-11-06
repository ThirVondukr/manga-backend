from typing import Optional

from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.engine import Result
from starlette.requests import Request

from db.dependencies import get_session
from db.models.users import User
from settings import auth as auth_settings


async def get_user_from_request(request: Request) -> Optional[User]:
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
