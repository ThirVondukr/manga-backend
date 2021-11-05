import pytest

from db.models.manga import Manga


@pytest.fixture
async def seed_manga(session) -> Manga:
    manga = Manga(
        title="Title",
        title_slug="title"
    )
    session.add(manga)
    await session.commit()
    await session.refresh(manga)
    yield manga
