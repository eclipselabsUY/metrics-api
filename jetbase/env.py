# Jetbase Configuration
# Update the sqlalchemy_url with your database connection string.

from dotenv import load_dotenv
import os

# Load Env Vars
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dotenv_path = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(dotenv_path)

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")
ENVIRONMENT = os.getenv("ENVIRONMENT")

if ENVIRONMENT == "DEV":
    def get_env_vars():
        return {
            "sqlalchemy_url": "sqlite+aiosqlite:///./egos.db",
            "async_mode": True,
        }
else:
    def get_env_vars():
        return {
            "sqlalchemy_url": f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}",
            "async_mode": True,
        }