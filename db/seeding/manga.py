from pathlib import Path

import slugify

from db.dependencies import get_session
from db.models.manga import Manga, MangaArt


async def seed_manga():
    async with get_session() as session:
        for image in Path("static/seeding/manga").iterdir():
            manga_cover = MangaArt(image_url=f"seeding/manga/{image.name}")
            manga = Manga(
                title=image.stem,
                title_slug=slugify.slugify(image.stem),
                arts=[manga_cover],
            )
            session.add(manga)
        await session.commit()
