import datetime
import typing
from typing import List, Optional
from uuid import UUID

import strawberry
from strawberry import LazyType
from strawberry.types import Info

from db.models.manga.chapters import MangaChapter

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
        loader = info.context["manga_loader"]
        return typing.cast(
            MangaType,
            await loader.load(self.manga_id),
        )

    @classmethod
    def from_orm(cls, chapter: MangaChapter):
        return cls(
            id=chapter.id,
            created_at=chapter.created_at,
            updated_at=chapter.updated_at,
            language=chapter.language,
            number=chapter.number,
            title=chapter.title,
            published_at=chapter.published_at,
            manga_id=chapter.manga_id,
        )


@strawberry.type
class LatestChaptersEdge:
    node: MangaChapterType
    cursor: datetime.datetime

    @classmethod
    def from_chapter(cls, chapter: MangaChapter) -> "LatestChaptersEdge":
        return cls(
            node=MangaChapterType.from_orm(chapter),
            cursor=chapter.published_at,
        )


@strawberry.type
class LatestChaptersPageInfo:
    end_cursor: Optional[datetime.datetime]
    has_next_page: bool


@strawberry.type
class LatestMangaChapters:
    edges: List[LatestChaptersEdge]
    page_info: LatestChaptersPageInfo
    total_count: int
