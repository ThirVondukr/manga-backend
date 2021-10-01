from functools import partial
from typing import Union, Optional, Any

import strawberry
from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL
from strawberry.dataloader import DataLoader

import gql
import gql.users
from gql import users
from gql.manga.info.loaders import load_manga_info
from gql.root import Root, Mutation
from gql.users import auth
from gql.users.auth import MaybeUser
from gql.users.loaders import load_is_liked_by_viewer, MangaLoaders


class MyGraphQL(GraphQL):
    async def get_context(
        self,
        request: Union[Request, WebSocket],
        response: Optional[Response] = None,
    ) -> Optional[Any]:
        ctx: dict = await super().get_context(request, response)

        user: MaybeUser = None
        if isinstance(request, Request):
            user = await auth.get_user_from_request(request=request)
            auth.put_user_into_context(ctx, user)

        ctx.update(
            {
                MangaLoaders.user_liked_manga_count: DataLoader(
                    users.loaders.load_user_liked_manga_count
                ),
                MangaLoaders.manga_is_liked_by_viewer: DataLoader(
                    partial(load_is_liked_by_viewer, user=user)
                ),
                "manga_loader": DataLoader(load_fn=gql.manga.manga.loaders.load_manga),
                "manga_info_loader": DataLoader(load_fn=load_manga_info),
                "manga_art_loader": DataLoader(
                    load_fn=gql.manga.art.loaders.load_manga_art
                ),
                "manga_cover_loader": DataLoader(
                    load_fn=gql.manga.art.loaders.load_manga_cover
                ),
                "manga_likes_loader": DataLoader(
                    load_fn=gql.manga.manga.loaders.load_manga_likes
                ),
                "manga_artists_loader": DataLoader(
                    load_fn=gql.manga.authors.loaders.load_manga_artists
                ),
                "manga_writers_loader": DataLoader(
                    load_fn=gql.manga.authors.loaders.load_manga_writers
                ),
            }
        )
        return ctx


graphql_app = MyGraphQL(schema=strawberry.Schema(query=Root, mutation=Mutation))
