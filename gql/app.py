from typing import Union, Optional

import strawberry
from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL

from gql.root import Root, Mutation
from gql.users.context import create_current_user_context
from . import context
from .extensions import DataLoadersExtension


class MyGraphQL(GraphQL):
    async def get_context(
        self,
        request: Union[Request, WebSocket],
        response: Optional[Response] = None,
    ) -> context.Context:
        create_current_user_context(request)
        return context.Context(
            request=request,
            response=response,
            loaders=None,  # type: ignore
        )


schema = strawberry.Schema(
    query=Root,
    mutation=Mutation,
    extensions=[DataLoadersExtension]
)
graphql_app = MyGraphQL(schema=schema)
