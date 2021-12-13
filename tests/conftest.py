import asyncio
import uuid
from contextlib import asynccontextmanager
from typing import Callable
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database

import db.dependencies
import settings
from app import create_app
from app.app import touch_models
from db.base import Base


@pytest.fixture(scope="session")
def event_loop():
    """I had some problems with event loop closing after first test, so hopefully this works"""
    loop = asyncio.get_event_loop()
    yield loop
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def __touch_models():
    """Load SQLAlchemy models so we can create all the tables using metadata"""
    touch_models()


@pytest.fixture(scope="session")
def db_name():
    """Random database name"""
    return str(uuid.uuid4())


@pytest.fixture(scope="session")
def db_sync_url(db_name):
    """Sync url for sync engine so we can create tables, and database"""
    return settings.test_database.get_sync_database_url(db_name)


@pytest.fixture(scope="session")
def db_async_url(db_name):
    return settings.test_database.get_database_url(db_name)


@pytest.fixture(scope="session", autouse=True)
def database(db_sync_url):
    create_database(db_sync_url)
    yield
    drop_database(db_sync_url)


@pytest.fixture(scope="session")
def sync_engine(db_sync_url, database):
    """Sync engine for easier database setup such as creating/dropping tables"""
    return create_engine(db_sync_url)


@pytest.fixture(scope="session")
def engine(db_async_url, database):
    return create_async_engine(db_async_url, future=True)


@pytest.fixture(scope="function", autouse=True)
def create_meta(sync_engine):
    try:
        Base.metadata.create_all(bind=sync_engine)
        yield
    finally:
        Base.metadata.drop_all(bind=sync_engine)


@pytest.fixture
async def session(engine) -> AsyncSession:
    async with engine.connect() as conn:
        try:
            transaction = await conn.begin()
            async with AsyncSession(future=True, bind=engine) as session:
                yield session
        finally:
            await transaction.rollback()


@pytest.fixture(autouse=True)
def patch_sessionmaker(session):
    """
    We patch db.dependencies._get_session with our sessionmaker
    so FastAPI and Strawberry use it instead
    """

    @asynccontextmanager
    async def get_session():
        yield session

    with patch.object(db.dependencies, "_get_session", new=get_session):
        yield


@pytest.fixture(scope="session")
def fastapi_app() -> FastAPI:
    return create_app()


@pytest.fixture(scope="session")
async def http_client(fastapi_app) -> AsyncClient:
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        yield client
