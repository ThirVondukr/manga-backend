from pathlib import Path

import slugify

from db.dependencies import get_session
from db.models.manga import Manga, MangaArt
from db.seeding import artists, info


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

            manga_info = info.create_manga_info(manga=manga)
            session.add(manga_info)

            author, relationships = artists.create_manga_author(manga=manga)
            session.add(author)
            session.add_all(relationships)
        await session.commit()
