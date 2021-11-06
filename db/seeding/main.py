import asyncio
from uuid import UUID

from db.base import Base
from db.dependencies import get_session
from db.models.users import User
from db.seeding import manga, chapters
from modules.auth.services import HashingService


async def clear_db():
    async with get_session() as session:
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()


async def create_user():
    async with get_session() as session:
        hash_service = HashingService()
        user = User(
            id=UUID("f75c6922-2d66-4480-b9c4-df325712c8a9"),
            username="Doctor",
            email="test@example.com",
        )
        hash_service.update_user_password(user, "3212")
        session.add(user)
        await session.commit()


async def main():
    await clear_db()
    await create_user()
    await manga.seed_manga()
    await chapters.seed_chapters()


if __name__ == "__main__":
    asyncio.run(main())
