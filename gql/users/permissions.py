from typing import Any

from strawberry import BasePermission

from gql.context import Info


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    async def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        user = await info.context.user()
        return user is not None
