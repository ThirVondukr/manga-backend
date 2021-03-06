import random
from pathlib import Path

import faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.dependencies import get_session
from db.models.manga import Manga, MangaChapter
from . import pages, ROOT_PATH

_fake = faker.Faker()


async def _seed_preset_manga_chapters(
    session: AsyncSession,
    manga_directory: Path,
):
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
            chapter_number = chapter_directory.stem.split(" ")[0]
            try:
                number, number_extra = chapter_number.split("-")
                number, number_extra = int(number), int(number_extra)
            except ValueError:
                number, number_extra = int(chapter_number), None
            chapter = MangaChapter(
                language="en",
                number=number,
                number_extra=number_extra,
                title=title,
                published_at=published_at,
            )
            manga.chapters.append(chapter)
            await pages.seed_preset_pages(
                chapter=chapter,
                chapter_directory=chapter_directory,
                session=session,
            )


async def _seed_manga_chapters(
    manga: Manga,
    session: AsyncSession,
):
    for chapter_number in range(1, random.randint(5, 15)):
        published_at = _fake.date_time_this_month()
        chapter = MangaChapter(
            language="en",
            number=chapter_number,
            number_extra=None,
            published_at=published_at,
            manga=manga,
        )
        session.add(chapter)


async def seed_chapters():
    async with get_session() as session:
        for directory in ROOT_PATH.joinpath("static/manga").iterdir():
            await _seed_preset_manga_chapters(session, directory)
        await session.commit()

        all_manga = (await session.execute(select(Manga))).scalars().all()
        for manga in all_manga:
            await _seed_manga_chapters(manga, session)
        await session.commit()
