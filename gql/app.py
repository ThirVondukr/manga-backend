from typing import Union, Optional, Any

import strawberry
from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL
from strawberry.dataloader import DataLoader

import gql.users
from gql import users
from gql.manga.info.loaders import load_manga_info
from gql.manga.pages.loaders import load_chapter_pages
from gql.root import Root, Mutation
from gql.users.context import create_current_user_context
from gql.users.loaders import load_is_liked_by_viewer, MangaLoaders


def _create_data_loaders():
    return {
        MangaLoaders.user_liked_manga_count: DataLoader(users.loaders.load_user_liked_manga_count),
        MangaLoaders.manga_is_liked_by_viewer: DataLoader(load_is_liked_by_viewer),
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
        "chapter_pages_loader": DataLoader(load_chapter_pages)
    }


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
