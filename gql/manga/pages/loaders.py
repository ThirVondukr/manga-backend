from collections import defaultdict
from typing import List
from uuid import UUID

from sqlalchemy import select

from db.dependencies import get_session
from db.models.manga import MangaPage


async def load_chapter_pages(chapter_ids: List[UUID]) -> List[List[MangaPage]]:
    query = select(MangaPage).filter(MangaPage.chapter_id.in_(chapter_ids)).order_by(MangaPage.number.asc())
    async with get_session() as session:
        pages: List[MangaPage] = (await session.scalars(query)).all()
    pages_by_chapter_id = defaultdict(list)
    for page in pages:
        pages_by_chapter_id[page.chapter_id].append(page)

    return [pages_by_chapter_id[chapter_id] for chapter_id in chapter_ids]
