from typing import List, Optional, Iterable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import load_only

from db.dependencies import get_session
from db.models.manga import Manga


async def load_manga(manga_ids: List[UUID]) -> List[Optional[Manga]]:
    query = select(Manga).filter(Manga.id.in_(manga_ids))
    async with get_session() as session:
        result: Result = await session.execute(query)

    manga_by_ids: dict[UUID, Manga] = {manga.id: manga for manga in result.scalars()}
    return [manga_by_ids.get(manga_id) for manga_id in manga_ids]


async def load_manga_likes(manga_ids: List[UUID]) -> List[int]:
    query = (
        select(Manga)
        .filter(Manga.id.in_(manga_ids))
        .options(load_only(Manga.id, Manga.likes_count))
    )

    async with get_session() as session:
        manga: Iterable[Manga] = await session.scalars(query)

    manga_likes_by_manga_id = {m.id: m.likes_count for m in manga}
    return [manga_likes_by_manga_id.get(manga_id, 0) for manga_id in manga_ids]
