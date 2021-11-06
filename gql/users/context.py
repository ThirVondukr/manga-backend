from typing import Optional, Union, Callable, Awaitable

from starlette.requests import Request
from starlette.websockets import WebSocket

from db.models.users import User
from gql.cache import AsyncCache
from gql.users.auth import get_user_from_request


async def _get_none() -> None:
    return None


def create_user_context(request: Union[Request, WebSocket]) -> Callable[..., Awaitable[Optional[User]]]:
    if isinstance(request, Request):
        return AsyncCache(lambda: get_user_from_request(request=request))
    return AsyncCache(_get_none)
