import datetime
from typing import Optional, List

from sqlalchemy import select

from db.dependencies import get_session
from db.models.manga import MangaLike
from db.models.manga.chapters import MangaChapter
from db.models.users import User
from gql.manga.chapters.types import MangaChapterType
from gql.pagination.types import Connection, PageInfo, Edge


async def resolve_latest_manga_chapters(
    first: int,
    after: Optional[datetime.datetime] = None,
) -> Connection[MangaChapterType, datetime.datetime]:
    # Query first + 1 entities to know if we have next page
    query = select(MangaChapter).order_by(MangaChapter.published_at.desc()).limit(first + 1)

    if after:
        query = query.filter(after > MangaChapter.published_at)

    async with get_session() as session:
        chapters = list(map(MangaChapterType.from_orm, await session.scalars(query)))

    if not chapters:
        return Connection(
            edges=[],
            page_info=PageInfo(None, False),
        )

    has_next_page = len(chapters) > first
    end_cursor = chapters[-2 if has_next_page else -1].published_at

    return Connection(
        edges=[Edge(node=chapter, cursor=chapter.published_at) for chapter in chapters],
        page_info=PageInfo(end_cursor, has_next_page),
    )


async def get_user_chapters_feed(
    user: User,
    first: int,
    after: Optional[datetime.datetime] = None,
) -> Connection[MangaChapterType, datetime.datetime]:
    query = (
        select(MangaChapter)
        .join(MangaLike, MangaLike.manga_id == MangaChapter.manga_id)
        .filter(MangaLike.user_id == user.id)
        .order_by(MangaChapter.published_at.desc())
        .limit(first + 1)
    )
    if after:
        query = query.filter(MangaChapter.published_at > after)

    async with get_session() as session:
        chapters: List[MangaChapter] = (await session.execute(query)).unique().scalars().all()

    has_next_page = len(chapters) > first
    chapters = chapters[:-1] if has_next_page else chapters
    chapter_types = [MangaChapterType.from_orm(c) for c in chapters]
    return Connection(
        edges=[Edge(node=chapter, cursor=chapter.published_at) for chapter in chapter_types],
        page_info=PageInfo(max(c.published_at for c in chapter_types), has_next_page),
    )
