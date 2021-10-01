import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.sql.functions import count

from db.dependencies import get_session
from db.models.manga import MangaLike
from db.models.manga.chapters import MangaChapter
from db.models.users import User
from gql.manga.chapters.types import (
    LatestChaptersEdge,
    LatestChaptersPageInfo,
    LatestMangaChapters,
)


async def resolve_latest_manga_chapters(
    first: int,
    after: Optional[datetime.datetime] = None,
) -> LatestMangaChapters:
    # Query first + 1 entities to know if we have next page
    query = (
        select(MangaChapter).order_by(MangaChapter.published_at.desc()).limit(first + 1)
    )
    if after:
        query = query.filter(after > MangaChapter.published_at)

    async with get_session() as session:
        total_count: int = (
            await session.execute(select(count(MangaChapter.id)))
        ).scalar_one()
        chapters_result = await session.execute(query)
        chapters = list(map(LatestChaptersEdge.from_chapter, chapters_result.scalars()))

        if not chapters:
            return LatestMangaChapters(
                edges=[],
                page_info=LatestChaptersPageInfo(None, False),
                total_count=total_count,
            )

    has_next_page = len(chapters) > first
    end_cursor = chapters[-2 if has_next_page else -1].node.published_at

    return LatestMangaChapters(
        edges=chapters[:first],
        page_info=LatestChaptersPageInfo(end_cursor, has_next_page),
        total_count=total_count,
    )


async def get_user_chapters_feed(
    user: User,
    first: int,
    after: Optional[datetime.datetime] = None,
) -> LatestMangaChapters:
    query = (
        select(MangaChapter)
        .join(MangaLike, MangaLike.manga_id == MangaChapter.manga_id)
        .filter(MangaLike.user_id == user.id)
        .order_by(MangaChapter.published_at.desc())
        .limit(first + 1)
    )
    total_count_query = select(count(MangaChapter.id)).join(
        MangaLike, MangaLike.manga_id == MangaChapter.manga_id
    )
    if after:
        query = query.filter(MangaChapter.published_at > after)

    async with get_session() as session:
        chapters: List[MangaChapter] = (
            (await session.execute(query)).unique().scalars().all()
        )
        total_count: int = (await session.execute(total_count_query)).scalar_one()

    has_next_page = len(chapters) > first

    edges = [LatestChaptersEdge.from_chapter(c) for c in chapters]
    edges = edges[:-1] if has_next_page else edges
    page_info = LatestChaptersPageInfo(
        has_next_page=has_next_page,
        end_cursor=max(c.published_at for c in chapters),
    )
    return LatestMangaChapters(
        edges=edges,
        page_info=page_info,
        total_count=total_count,
    )
