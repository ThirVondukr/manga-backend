from __future__ import annotations

import datetime
import typing
from typing import Optional, List
from uuid import UUID

import strawberry
from strawberry import LazyType
from strawberry.types import Info

from db.models.manga.chapters import MangaChapter
from gql._loaders import Loaders
from gql.manga.pages.types import MangaPageType

MangaType = LazyType["MangaType", "gql.manga.manga.types"]


@strawberry.type(name="MangaChapter")
class MangaChapterType:
    id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    language: str
    number: str
    title: Optional[str]
    published_at: datetime.datetime

    manga_id: UUID

    @strawberry.field
    async def manga(self, info: Info) -> MangaType:
        loader = info.context[Loaders.manga]
        return typing.cast(
            MangaType,
            await loader.load(self.manga_id),
        )

    @strawberry.field
    async def pages(self, info: Info) -> List[MangaPageType]:
        loader = info.context[Loaders.chapter_pages]
        return await loader.load(self.id)

    @classmethod
    def from_orm(cls, model: MangaChapter) -> MangaChapterType:
        return cls(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            language=model.language,
            number=model.number,
            title=model.title,
            published_at=model.published_at,
            manga_id=model.manga_id,
        )
