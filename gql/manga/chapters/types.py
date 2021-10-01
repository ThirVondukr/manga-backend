import datetime
import typing
from typing import List, Optional
from uuid import UUID

import strawberry
from sqlalchemy import select, cast, func, Integer
from sqlalchemy.engine import Result
from sqlalchemy.sql.functions import count
from strawberry import Private, LazyType
from strawberry.types import Info

from db.dependencies import get_session
from db.models.manga.chapters import MangaChapter
from gql.pagination.types import PaginationPydantic, PaginationInput

MangaType = LazyType["MangaType", "gql.manga.manga.types"]


def resolve_recent_chapters(pagination: PaginationInput) -> "RecentChapters":
    pagination = pagination.to_pydantic()
    return RecentChapters(
        page=pagination.page,
        page_size=pagination.page_size,
        pagination=pagination,
    )


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
class RecentChapters:
    pagination: Private[PaginationPydantic]

    page: int
    page_size: int

    @strawberry.field
    async def chapters(self) -> List[MangaChapterType]:
        query = select(MangaChapter).order_by(
            cast((func.substring(MangaChapter.number, "^[0-9]+")), Integer).desc(),
            MangaChapter.number.desc(),
        )
        query = self.pagination.apply_to_query(query)

        async with get_session() as session:
            result: Result = await session.execute(query)
        return result.scalars().all()

    @strawberry.field
    async def total_count(self) -> int:
        async with get_session() as session:
            result: Result = await session.execute(select(count(MangaChapter.id)))
        return typing.cast(int, result.scalar_one())


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
