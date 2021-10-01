import strawberry

from . import manga
from .manga.chapters.root import ChaptersRoot
from .manga.manga.root import MangaRoot
from .users.root import UsersRoot


@strawberry.type
class Root(
    ChaptersRoot,
    MangaRoot,
    UsersRoot,
):
    pass


@strawberry.type
class Mutation(
    manga.manga.mutations.Mutation,
):
    pass
