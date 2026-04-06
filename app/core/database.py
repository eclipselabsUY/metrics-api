from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from contextlib import contextmanager
from aiochclient import ChClient
from aiohttp import ClientSession

from app.core.config import (
    DATABASE_URL,
    CLICKHOUSE_URL,
    CLICKHOUSE_DB,
    CLICKHOUSE_USER,
    CLICKHOUSE_PASSWORD,
)


class Base(DeclarativeBase):
    pass


# Async DB

async_engine = create_async_engine(DATABASE_URL, echo=False, future=True)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session


# Sync DB

SYNC_DATABASE_URL = DATABASE_URL.replace("+aiosqlite", "").replace("+asyncpg", "")

sync_engine = create_engine(SYNC_DATABASE_URL, echo=False, future=True)

SyncSessionLocal = sessionmaker(bind=sync_engine, expire_on_commit=False)


@contextmanager
def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ClickHouse DB

_ch_session = None
_ch_client = None


async def get_clickhouse_client() -> ChClient:
    global _ch_client, _ch_session
    if _ch_client is None:
        _ch_session = ClientSession()
        _ch_client = ChClient(
            _ch_session,
            url=CLICKHOUSE_URL,
            user=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DB,
        )
    return _ch_client


async def close_clickhouse_client():
    global _ch_client, _ch_session
    if _ch_session:
        await _ch_session.close()
        _ch_session = None
        _ch_client = None
