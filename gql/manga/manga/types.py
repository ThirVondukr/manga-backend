import typing
from typing import cast, List, Optional
from uuid import UUID

import strawberry

from db.models.manga import Manga
from gql.context import Info
from gql.manga.art.types import MangaArtType
from gql.manga.authors.types import AuthorType
from gql.manga.chapters.chapters import (
    MangaChaptersPaginationResponse,
    get_manga_chapters,
)
from gql.manga.info.types import MangaInfoType
from gql.pagination.types import PaginationInput


@strawberry.type(name="Manga")
class MangaType:
    id: UUID
    title: str
    title_slug: str

    @classmethod
    def from_orm(cls, manga: Manga):
        return cls(
            id=manga.id,
            title=manga.title,
            title_slug=manga.title_slug,
        )

    @strawberry.field
    async def is_liked_by_viewer(self, info: Info) -> bool:
        return await info.context.loaders.manga_is_liked_by_viewer.load(self.id)

    @strawberry.field
    async def likes_count(self, info: Info) -> int:
        return await info.context.loaders.manga_likes_count.load(self.id)

    @strawberry.field
    async def artists(self, info: Info) -> List[AuthorType]:
        return await info.context.loaders.manga_artists.load(self.id)

    @strawberry.field
    async def writers(self, info: Info) -> List[AuthorType]:
        return await info.context.loaders.manga_writers.load(self.id)

    @strawberry.field
    async def arts(self, info: Info) -> List[MangaArtType]:
        return await info.context.loaders.manga_arts.load(self.id)

    @strawberry.field
    async def cover(self, info: Info) -> Optional[MangaArtType]:
        return await info.context.loaders.manga_cover.load(self.id)

    @strawberry.field
    async def infos(self, info: Info) -> List[MangaInfoType]:
        return await info.context.loaders.manga_infos.load(self.id)

    @strawberry.field
    async def chapters(self, pagination: PaginationInput) -> MangaChaptersPaginationResponse:
        return await get_manga_chapters(cast(Manga, self).id, pagination)
