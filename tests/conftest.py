import asyncio
import os

import dotenv
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from hypothesis import settings as hypothesis_settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app import create_app
from app.app import touch_models
from db.base import Base, Session

hypothesis_settings.register_profile("dev", max_examples=10)
hypothesis_settings.load_profile("dev")

hypothesis_settings.register_profile("ci", max_examples=100)

dotenv.load_dotenv()


@pytest.fixture(scope="session")
def event_loop():
    """Make event loop session-scoped"""
    loop = asyncio.get_event_loop()
    yield loop
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def __touch_models():
    """Load SQLAlchemy models so we can create all the tables using metadata"""
    touch_models()


@pytest.fixture(scope="session")
def engine():
    return create_async_engine(
        url=os.environ["TEST_DATABASE_URL"],
        future=True
    )


@pytest.fixture(scope="session", autouse=True)
async def create_meta(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True)
async def session(engine) -> AsyncSession:
    async with engine.connect() as conn:
        transaction = await conn.begin()
        Session.configure(bind=conn)
        yield Session()
        await transaction.rollback()


@pytest.fixture(scope="session")
def fastapi_app() -> FastAPI:
    return create_app()


@pytest.fixture(scope="session")
async def http_client(fastapi_app) -> AsyncClient:
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        yield client
