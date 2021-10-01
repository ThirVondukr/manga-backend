from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result

from db.dependencies import get_session
from db.models.manga import Manga
from gql.manga.manga.types import MangaType


async def get_manga_by_id(manga_id: UUID) -> Optional[MangaType]:
    query = select(Manga).filter(Manga.id == manga_id).limit(1)
    async with get_session() as session:
        result: Result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_manga_by_title_slug(title_slug: str) -> Optional[MangaType]:
    query = select(Manga).filter(Manga.title_slug == title_slug).limit(1)
    async with get_session() as session:
        result: Result = await session.execute(query)
    return result.scalar_one_or_none()


async def search_manga(title_like: str = "") -> List[MangaType]:
    query = select(Manga)
    if title_like:
        query = query.filter(Manga.title.ilike(f"%{title_like}%"))

    async with get_session() as session:
        result = await session.execute(query)

    return [MangaType.from_orm(m) for m in result.scalars()]


async def popular_manga() -> List[MangaType]:
    query = select(Manga).order_by(Manga.likes_count.desc()).limit(10)

    async with get_session() as session:
        result = await session.execute(query)

    return [MangaType.from_orm(m) for m in result.scalars()]
