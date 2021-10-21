from typing import Union, Optional, Any

import strawberry
from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL

from gql._loaders import _create_data_loaders
from gql.root import Root, Mutation
from gql.users.context import create_current_user_context


class MyGraphQL(GraphQL):
    async def get_context(
        self,
        request: Union[Request, WebSocket],
        response: Optional[Response] = None,
    ) -> Optional[Any]:
        ctx: dict = await super().get_context(request, response)

        create_current_user_context(request)
        ctx.update(_create_data_loaders())
        return ctx


graphql_app = MyGraphQL(schema=strawberry.Schema(query=Root, mutation=Mutation))
