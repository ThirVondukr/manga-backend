from collections import defaultdict
from typing import List, Iterable
from uuid import UUID

from sqlalchemy import select

from db.dependencies import get_session
from db.models.manga import MangaInfo


async def manga_infos(manga_ids: List[UUID]) -> List[List[MangaInfo]]:
    query = select(MangaInfo).filter(MangaInfo.manga_id.in_(manga_ids))
    async with get_session() as session:
        infos: Iterable[MangaInfo] = (await session.execute(query)).scalars()

    infos_by_manga_id = defaultdict(list)
    for info in infos:
        infos_by_manga_id[info.manga_id].append(info)
    return [infos_by_manga_id[manga_id] for manga_id in manga_ids]
