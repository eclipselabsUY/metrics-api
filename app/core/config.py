from dotenv import load_dotenv
import os

# Load Env Vars
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
dotenv_path = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(dotenv_path)

# Current EGO Services
SERVICES = [
    {"name": "www.ego-services.com", "type": "http", "url": "https://www.ego-services.com"},
    {"name": "backdoor.ego-services.com", "type": "http", "url": "https://backdoor.ego-services.com/health"},
    {"name": "fingcraft.ego-services.com", "type": "tcp", "host": "fingcraft.ego-services.com", "port": 25565},
    {"name": "ssh.ego-services.com", "type": "tcp", "host": "ssh.ego-services.com", "port": 22},
    {"name": "api.ego-services.com", "type": "http", "url": "http://api.ego-services.com/health"},
]

# Keys and Passwords
API_KEY = os.getenv("API_KEY")
RCON_PASSWORD = os.getenv("RCON_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")

ENVIRONMENT = os.getenv("ENVIRONMENT")

if ENVIRONMENT == "DEV":
    DATABASE_URL = "sqlite+aiosqlite:///./egos.db"
else:
    DATABASE_URL = (
        f"postgresql+asyncpg://"
        f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}"
        f"/{POSTGRES_DB}"
    )