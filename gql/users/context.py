from contextvars import ContextVar
from typing import Optional, Union

from starlette.requests import Request
from starlette.websockets import WebSocket

from db.models.users import User
from gql.cache import AsyncCache
from gql.users.auth import get_user_from_request

current_user_var = ContextVar("current_user_var")


async def _get_none() -> None:
    return None


async def get_current_user_from_context() -> Optional[User]:
    return await current_user_var.get()


def create_current_user_context(request: Union[Request, WebSocket]):
    if isinstance(request, Request):
        current_user_var.set(AsyncCache(lambda: get_user_from_request(request=request)))
    else:
        current_user_var.set(AsyncCache(_get_none))
