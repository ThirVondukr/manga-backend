from __future__ import annotations

import math
from typing import List
from uuid import UUID

import strawberry
from sqlalchemy import select, cast, func, Integer
from sqlalchemy.engine import Result
from sqlalchemy.sql import Select
from sqlalchemy.sql.functions import count

from db.dependencies import get_session
from db.models.manga.chapters import MangaChapter
from gql.manga.chapters.types import MangaChapterType
from gql.pagination.types import (
    PagePaginationPageInfo,
    PaginationPydantic,
    PaginationInput,
)


@strawberry.type
class MangaChaptersPaginationResponse:
    page_info: PagePaginationPageInfo
    items: List[MangaChapterType]


async def get_manga_chapters(
    manga_id: UUID,
    pagination: PaginationInput,
) -> MangaChaptersPaginationResponse:
    pagination_pydantic: PaginationPydantic = pagination.to_pydantic()
    chapters_query: Select = (
        select(MangaChapter)
        .order_by(
            cast((func.substring(MangaChapter.number, "^[0-9]+")), Integer).desc(),
            MangaChapter.number.desc(),
        )
        .filter(MangaChapter.manga_id == manga_id)
    )
    chapters_query = pagination_pydantic.apply_to_query(chapters_query)
    total_count_query = select(count(MangaChapter.id)).filter(
        MangaChapter.manga_id == manga_id
    )

    async with get_session() as session:
        chapters: Result = await session.execute(chapters_query)
        total_count: int = (await session.execute(total_count_query)).scalar_one()

    return MangaChaptersPaginationResponse(
        items=chapters.scalars().all(),
        page_info=PagePaginationPageInfo(
            has_next=total_count
            > pagination_pydantic.page * pagination_pydantic.page_size,
            page=pagination_pydantic.page,
            page_size=pagination_pydantic.page_size,
            total_pages=math.ceil(total_count / pagination_pydantic.page_size),
            total_count=total_count,
        ),
    )
