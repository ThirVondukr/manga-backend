from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

import db.base


@asynccontextmanager
async def _get_session() -> AsyncGenerator[AsyncSession, None]:
    async with db.base.Session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with _get_session() as session:
        yield session


async def get_session_dependency() -> AsyncGenerator[AsyncSession, None]:
    async with _get_session() as session:
        yield session
