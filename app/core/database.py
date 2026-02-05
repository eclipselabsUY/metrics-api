from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from contextlib import contextmanager

from app.core.config import DATABASE_URL

class Base(DeclarativeBase):
    pass

# Async DB

async_engine = create_async_engine(DATABASE_URL, echo = False, future = True)

AsyncSessionLocal = async_sessionmaker(
    bind = async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session

# Sync DB

SYNC_DATABASE_URL = DATABASE_URL.replace("+aiosqlite", "").replace("+asyncpg", "")

sync_engine = create_engine(SYNC_DATABASE_URL, echo=False, future=True)

SyncSessionLocal = sessionmaker(
    bind = sync_engine,
    expire_on_commit=False
)

@contextmanager
def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
