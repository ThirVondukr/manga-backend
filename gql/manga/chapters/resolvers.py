import datetime
from typing import Optional, List
from uuid import UUID

from sqlalchemy import select

from db.dependencies import get_session
from db.models.manga import MangaLike
from db.models.manga.chapters import MangaChapter
from db.models.users import User
from gql.manga.chapters.types import MangaChapterType
from gql.pagination.pagination import CursorPaginator
from gql.pagination.types import Connection, PageInfo, Edge


async def resolve_latest_manga_chapters(
    first: int,
    after: Optional[datetime.datetime] = None,
) -> Connection[MangaChapterType]:
    # Query first + 1 entities to know if we have next page
    query = select(MangaChapter).order_by(MangaChapter.published_at.desc()).limit(first + 1)

    if after:
        query = query.filter(MangaChapter.published_at <= after)

    async with get_session() as session:
        chapters = list(await session.scalars(query))

    paginator = CursorPaginator(
        type_cls=MangaChapterType,
        cursor_func=lambda c: str(c.published_at),
    )
    return paginator.parse_sequence(
        sequence=chapters,
        first=first,
    )


async def get_user_chapters_feed(
    user: User,
    first: int,
    after: Optional[datetime.datetime] = None,
) -> Connection[MangaChapterType]:
    query = (
        select(MangaChapter)
        .join(MangaLike, MangaLike.manga_id == MangaChapter.manga_id)
        .filter(MangaLike.user_id == user.id)
        .order_by(MangaChapter.published_at.desc())
        .limit(first + 1)
    )
    if after:
        query = query.filter(MangaChapter.published_at < after)

    async with get_session() as session:
        chapters: List[MangaChapter] = (await session.execute(query)).unique().scalars().all()

    has_next_page = len(chapters) > first
    chapters = chapters[:-1] if has_next_page else chapters
    chapter_types = [MangaChapterType.from_orm(c) for c in chapters]
    if not chapter_types:
        return Connection([], page_info=PageInfo("", False))

    return Connection(
        edges=[
            Edge(
                node=chapter,
                cursor=str(chapter.published_at),
            )
            for chapter in chapter_types
        ],
        page_info=PageInfo(
            end_cursor=str(chapter_types[-1].published_at),
            has_next_page=has_next_page,
        ),
    )


async def get_chapter_by_id(chapter_id: UUID) -> MangaChapterType:
    query = select(MangaChapter).filter(MangaChapter.id == chapter_id)
    async with get_session() as session:
        chapter: MangaChapter = await session.scalar(query)

    return MangaChapterType.from_orm(chapter)
