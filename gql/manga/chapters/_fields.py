from __future__ import annotations

from typing import List, Iterable, TYPE_CHECKING, Optional

from sqlalchemy import select, func
from strawberry import LazyType

from db.dependencies import get_session
from db.models.manga import MangaChapter

if TYPE_CHECKING:
    from .types import MangaChapterType

LazyMangaChapterType = LazyType["MangaChapterType", ".types"]


async def all_chapters(self: MangaChapterType) -> List[LazyMangaChapterType]:
    query = (
        select(MangaChapter)
        .filter(MangaChapter.manga_id == self.manga_id)
        .order_by(MangaChapter.number, func.coalesce(MangaChapter.number_extra, 0))
    )
    async with get_session() as session:
        chapters: Iterable[MangaChapter] = await session.scalars(query)
    return self.from_orm_list(chapters)


async def previous(self: MangaChapterType) -> Optional[LazyMangaChapterType]:
    query = (
        select(MangaChapter)
        .filter(
            MangaChapter.id != self.id,
            MangaChapter.number <= self.number,
            func.coalesce(MangaChapter.number_extra, 0) <= func.coalesce(self.number_extra, 0),
        )
        .order_by(MangaChapter.number.desc(), func.coalesce(MangaChapter.number_extra, 0).desc())
        .limit(1)
    )
    async with get_session() as session:
        chapter: Optional[MangaChapter] = (await session.scalars(query)).one_or_none()
    return self.from_orm_optional(chapter)


async def next_(self) -> Optional[LazyMangaChapterType]:
    query = (
        select(MangaChapter)
        .filter(
            MangaChapter.id != self.id,
            MangaChapter.number >= self.number,
            func.coalesce(MangaChapter.number_extra, 0) >= func.coalesce(self.number_extra, 0),
        )
        .order_by(MangaChapter.number, func.coalesce(MangaChapter.number_extra, 0))
        .limit(1)
    )
    async with get_session() as session:
        chapter: Optional[MangaChapter] = (await session.scalars(query)).one_or_none()
    return self.from_orm_optional(chapter)
