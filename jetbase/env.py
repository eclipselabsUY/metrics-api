# Jetbase Configuration
# Update the sqlalchemy_url with your database connection string.

from app.core.config import JETBASE_SQLALCHEMY_URL, ASYNC

sqlalchemy_url = JETBASE_SQLALCHEMY_URL
async_mode = ASYNC

print(sqlalchemy_url)
print(f"Async: {async_mode}")