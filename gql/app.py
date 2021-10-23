from typing import Union, Optional

import strawberry
from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL

from gql.root import Query, Mutation
from gql.users.context import create_user_context
from .context import Context, context_var
from .extensions import DataLoadersExtension


class MyGraphQL(GraphQL):
    async def get_context(
        self,
        request: Union[Request, WebSocket],
        response: Optional[Response] = None,
    ) -> Context:
        context = Context(
            request=request,
            response=response,
            loaders=None,  # type: ignore
            user=create_user_context(request),
        )
        context_var.set(context)
        return context


schema = strawberry.Schema(query=Query, mutation=Mutation, extensions=[DataLoadersExtension])
graphql_app = MyGraphQL(schema=schema)
