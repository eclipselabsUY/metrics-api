from app.core.config import DATABASE_URL, JETBASE_SQLALCHEMY_URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


sync_url = JETBASE_SQLALCHEMY_URL if JETBASE_SQLALCHEMY_URL else DATABASE_URL

sync_engine = create_engine(sync_url)
SyncSessionLocal = sessionmaker(bind=sync_engine, expire_on_commit=False)


def start_db_engine():
    engine = create_async_engine(DATABASE_URL)
    return engine
