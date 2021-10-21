from collections import defaultdict
from typing import List, Iterable, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result

from db.dependencies import get_session
from db.models.manga.art import MangaArt


async def manga_arts(manga_ids: List[UUID]) -> List[List[MangaArt]]:
    query = select(MangaArt).filter(MangaArt.manga_id.in_(manga_ids))
    async with get_session() as session:
        result: Result = await session.execute(query)
    manga_arts: Iterable[MangaArt] = result.scalars()

    arts: dict[UUID, List[MangaArt]] = defaultdict(list)
    for manga_art in manga_arts:
        arts[manga_art.manga_id].append(manga_art)

    return [arts[manga_id] for manga_id in manga_ids]


async def manga_cover(manga_ids: List[UUID]) -> List[Optional[MangaArt]]:
    query = select(MangaArt).filter(MangaArt.manga_id.in_(manga_ids))

    async with get_session() as session:
        arts: Iterable[MangaArt] = (await session.execute(query)).scalars()
    arts_by_manga_ids: dict[UUID, MangaArt] = {art.manga_id: art for art in arts}

    return [arts_by_manga_ids.get(manga_id) for manga_id in manga_ids]
