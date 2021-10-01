import typing
from typing import cast, List, Optional
from uuid import UUID

import strawberry
from strawberry.types import Info

from db.models.manga import Manga
from gql.manga.art.types import MangaArtType
from gql.manga.authors.types import AuthorType
from gql.manga.chapters.chapters import (
    MangaChaptersPaginationResponse,
    get_manga_chapters,
)
from gql.manga.info.types import MangaInfoType
from gql.pagination.types import PaginationInput
from gql.users.loaders import MangaLoaders


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
        return cast(
            bool,
            await info.context[MangaLoaders.manga_is_liked_by_viewer].load(self.id),
        )

    @strawberry.field
    async def likes_count(self, info: Info) -> int:
        loader = info.context["manga_likes_loader"]
        return cast(int, await loader.load(self.id))

    @strawberry.field
    async def artists(self, info: Info) -> List[AuthorType]:
        loader = info.context["manga_artists_loader"]
        return typing.cast(List[AuthorType], await loader.load(self.id))

    @strawberry.field
    async def writers(self, info: Info) -> List[AuthorType]:
        loader = info.context["manga_writers_loader"]
        return typing.cast(List[AuthorType], await loader.load(self.id))

    @strawberry.field
    async def arts(self, info: Info) -> List[MangaArtType]:
        loader = info.context["manga_art_loader"]
        return typing.cast(
            List[MangaArtType],
            await loader.load(self.id),
        )

    @strawberry.field
    async def cover(self, info: Info) -> Optional[MangaArtType]:
        loader = info.context["manga_cover_loader"]
        return typing.cast(
            Optional[MangaArtType],
            await loader.load(self.id),
        )

    @strawberry.field
    async def infos(self, info: Info) -> List[MangaInfoType]:
        loader = info.context["manga_info_loader"]
        return typing.cast(
            List[MangaInfoType],
            await loader.load(self.id),
        )

    @strawberry.field
    async def chapters(
        self, pagination: PaginationInput
    ) -> MangaChaptersPaginationResponse:
        return await get_manga_chapters(cast(Manga, self).id, pagination)
