from __future__ import annotations

import datetime
from typing import Optional, List, Iterable
from uuid import UUID

import strawberry
from sqlalchemy import select, func
from strawberry import LazyType

from db.dependencies import get_session
from db.models.manga.chapters import MangaChapter
from gql.context import Info
from gql.manga.pages.types import MangaPageType
from gql.mixins import OrmTypeMixin

MangaType = LazyType["MangaType", "gql.manga.manga.types"]


@strawberry.type(name="MangaChapter")
class MangaChapterType(OrmTypeMixin):
    id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    language: str
    number: int
    number_extra: Optional[int]
    title: Optional[str]
    published_at: datetime.datetime

    manga_id: UUID
    instance: strawberry.Private[str]

    @strawberry.field
    async def all_chapters(self) -> List[MangaChapterType]:
        query = (
            select(MangaChapter)
            .filter(MangaChapter.manga_id == self.manga_id)
            .order_by(MangaChapter.number, func.coalesce(MangaChapter.number_extra, 0))
        )

        async with get_session() as session:
            chapters: Iterable[MangaChapter] = await session.scalars(query)
        return self.from_orm_list(chapters)

    @strawberry.field
    async def previous(self) -> Optional[MangaChapterType]:
        query = (
            select(MangaChapter)
            .filter(
                MangaChapter.id != self.id,
                MangaChapter.number <= self.number,
                func.coalesce(MangaChapter.number_extra, 0)
                <= func.coalesce(self.number_extra, 0),
            )
            .order_by(
                MangaChapter.number.desc(), func.coalesce(MangaChapter.number_extra, 0).desc()
            )
            .limit(1)
        )
        async with get_session() as session:
            chapter: Optional[MangaChapter] = (await session.scalars(query)).one_or_none()
        return self.from_orm_optional(chapter)

    @strawberry.field
    async def next(self) -> Optional[MangaChapterType]:
        query = (
            select(MangaChapter)
            .filter(
                MangaChapter.id != self.id,
                MangaChapter.number >= self.number,
                func.coalesce(MangaChapter.number_extra, 0)
                >= func.coalesce(self.number_extra, 0),
            )
            .order_by(MangaChapter.number, func.coalesce(MangaChapter.number_extra, 0))
            .limit(1)
        )
        async with get_session() as session:
            chapter: Optional[MangaChapter] = (await session.scalars(query)).one_or_none()
        return self.from_orm_optional(chapter)

    @strawberry.field
    async def manga(self, info: Info) -> MangaType:
        return await info.context.loaders.manga.load(self.manga_id)

    @strawberry.field
    async def pages(self, info: Info) -> List[MangaPageType]:
        pages = await info.context.loaders.chapter_pages.load(self.id)
        return [MangaPageType.from_orm(page) for page in pages]

    @classmethod
    def from_orm(cls, model: MangaChapter) -> MangaChapterType:
        return cls(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            language=model.language,
            number=model.number,
            number_extra=model.number_extra,
            title=model.title,
            published_at=model.published_at,
            manga_id=model.manga_id,
        )
