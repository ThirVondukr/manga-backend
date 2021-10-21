from typing import Union, Optional, Any

import strawberry
from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL
from strawberry.dataloader import DataLoader

from gql import users
from gql._loaders import Loaders
from gql.manga import manga, info, art, authors, pages

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


def _create_data_loaders():
    return {
        Loaders.manga: DataLoader(manga.loaders.load_manga),
        Loaders.manga_infos: DataLoader(info.loaders.manga_infos),
        Loaders.manga_arts: DataLoader(art.loaders.manga_arts),
        Loaders.manga_cover: DataLoader(art.loaders.manga_cover),
        Loaders.manga_likes_count: DataLoader(manga.loaders.manga_likes),
        Loaders.manga_artists: DataLoader(authors.loaders.manga_artists),
        Loaders.manga_writers: DataLoader(authors.loaders.manga_writers),
        Loaders.manga_is_liked_by_viewer: DataLoader(users.loaders.manga_is_liked_by_viewer),
        Loaders.user_liked_manga_count: DataLoader(users.loaders.user_liked_manga_count),
        Loaders.chapter_pages: DataLoader(pages.loaders.load_chapter_pages)
    }
