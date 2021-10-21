import enum


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


