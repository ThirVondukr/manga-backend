import enum

from strawberry.dataloader import DataLoader

from gql import users
from gql.manga import art, authors, info, manga, pages


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
