from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from db.base import Session

get_session = Session


async def get_session_dependency() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session
