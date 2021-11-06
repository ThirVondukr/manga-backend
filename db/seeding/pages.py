from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from db.models.manga import MangaChapter, MangaPage
from db.seeding import ROOT_PATH


async def seed_preset_pages(
    *,
    chapter: MangaChapter,
    chapter_directory: Path,
    session: AsyncSession,
):
    pages = []
    for page_number, page_path in enumerate(chapter_directory.iterdir(), start=1):
        relative_path = page_path.relative_to(ROOT_PATH.joinpath("static"))
        page = MangaPage(
            image_url=str(relative_path).replace("\\", "/"),
            chapter=chapter,
            number=page_number,
        )
        pages.append(page)
    session.add_all(pages)
