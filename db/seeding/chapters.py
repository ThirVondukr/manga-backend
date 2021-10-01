import random
from pathlib import Path

import faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.dependencies import get_session
from db.models.manga import Manga, MangaChapter

_fake = faker.Faker()


async def _seed_preset_manga_chapters(session: AsyncSession, manga_directory: Path):
    query = (
        select(Manga)
        .options(selectinload(Manga.chapters))
        .filter(Manga.title_slug == manga_directory.stem)
        .limit(1)
    )
    manga = await session.scalar(query)
    for volume_directory in manga_directory.iterdir():
        for chapter_directory in volume_directory.iterdir():
            title = None
            if len(s := chapter_directory.stem.split(" ")) > 2:
                title = s[1]

            published_at = _fake.date_time_this_month()

            chapter = MangaChapter(
                language="en",
                number=chapter_directory.stem.split(" ")[0],
                title=title,
                published_at=published_at,
            )
            manga.chapters.append(chapter)


async def _seed_manga_chapters(
    manga: Manga,
    session: AsyncSession,
):
    for chapter_number in range(1, random.randint(5, 15)):
        published_at = _fake.date_time_this_month()
        chapter = MangaChapter(
            language="en",
            number=str(chapter_number),
            published_at=published_at,
            manga=manga,
        )
        session.add(chapter)


async def seed_chapters():
    async with get_session() as session:
        for directory in Path("static/manga").iterdir():
            await _seed_preset_manga_chapters(session, directory)
        await session.commit()

        all_manga = (await session.execute(select(Manga))).scalars().all()
        for manga in all_manga:
            await _seed_manga_chapters(manga, session)
        await session.commit()
