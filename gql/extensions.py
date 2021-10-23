from graphql.pyutils import AwaitableOrValue
from strawberry.dataloader import DataLoader
from strawberry.extensions import Extension

from gql import users
from gql.manga import manga, info, art, authors, pages
from . import context


class DataLoadersExtension(Extension):
    def on_request_start(self) -> AwaitableOrValue[None]:
        self.execution_context.context.loaders = context.Loaders(
            manga=DataLoader(manga.loaders.load_manga),
            manga_infos=DataLoader(info.loaders.manga_infos),
            manga_arts=DataLoader(art.loaders.manga_arts),
            manga_cover=DataLoader(art.loaders.manga_cover),
            manga_artists=DataLoader(authors.loaders.manga_artists),
            manga_writers=DataLoader(authors.loaders.manga_writers),
            manga_likes_count=DataLoader(manga.loaders.manga_likes),
            manga_is_liked_by_viewer=DataLoader(users.loaders.manga_is_liked_by_viewer),
            user_liked_manga_count=DataLoader(users.loaders.user_liked_manga_count),
            chapter_pages=DataLoader(pages.loaders.load_chapter_pages),
        )
        return None
