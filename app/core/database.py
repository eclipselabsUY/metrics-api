from sqlalchemy import create_async_engine

from app.core.config import DATABASE_URL

def start_db_engine():
    engine = create_async_engine(DATABASE_URL)
    return engine