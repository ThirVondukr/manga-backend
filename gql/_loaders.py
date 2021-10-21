import enum

from strawberry.dataloader import DataLoader

import gql.manga
from gql import users
from gql.manga.info.loaders import load_manga_infos
from gql.manga.pages.loaders import load_chapter_pages
from gql.users.loaders import load_is_liked_by_viewer


class Loaders(enum.Enum):
    manga = enum.auto()
    manga_infos = enum.auto()
    manga_arts = enum.auto()
    manga_cover = enum.auto()
    manga_likes_count = enum.auto()
    manga_artists = enum.auto()
    manga_writers = enum.auto()
    manga_is_liked_by_viewer = enum.auto()

    user_liked_manga_count = enum.auto()

    chapter_pages = enum.auto()


def _create_data_loaders():
    return {
        Loaders.user_liked_manga_count: DataLoader(users.loaders.load_user_liked_manga_count),
        Loaders.manga_is_liked_by_viewer: DataLoader(load_is_liked_by_viewer),
        Loaders.manga: DataLoader(gql.manga.manga.loaders.load_manga),
        Loaders.manga_infos: DataLoader(load_manga_infos),
        Loaders.manga_arts: DataLoader(gql.manga.art.loaders.load_manga_arts),
        Loaders.manga_cover: DataLoader(gql.manga.art.loaders.load_manga_cover),
        Loaders.manga_likes_count: DataLoader(gql.manga.manga.loaders.load_manga_likes),
        Loaders.manga_artists: DataLoader(gql.manga.authors.loaders.load_manga_artists),
        Loaders.manga_writers: DataLoader(gql.manga.authors.loaders.load_manga_writers),
        Loaders.chapter_pages: DataLoader(load_chapter_pages)
    }
