from strawberry.tools import merge_types

from .manga.chapters.query import ChaptersQuery
from .manga.manga.mutations import MangaMutation
from .manga.manga.query import MangaQuery
from .users.query import UsersQuery

Query = merge_types("Root", (ChaptersQuery, MangaQuery, UsersQuery))
Mutation = merge_types("Mutation", (MangaMutation,))
