import hmac
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import secrets
from fastapi import HTTPException, Header
from app.core.config import ADMIN_API_KEY
from typing import cast

ph = PasswordHasher()


# Generate apikey
def generate_api_key() -> tuple[str, str, str]:
    """
    Returns:
        full_key (str)
        prefix (str)
        secret (str)
    """
    prefix = secrets.token_hex(4)  # 8 hex chars
    secret = secrets.token_urlsafe(32)

    full_key = f"egos_{prefix}.{secret}"

    return full_key, prefix, secret


# hasher
def hash_api_key(secret: str) -> str:
    return ph.hash(secret)


# verify key
def verify_api_key(secret: str, hashed_key: str) -> bool:
    try:
        ph.verify(hashed_key, secret)
        return True
    except VerifyMismatchError:
        return False


async def verify_admin_key(x_admin_key: str = Header(...)):
    admin_key = cast(str, ADMIN_API_KEY)
    if not admin_key:
        raise HTTPException(500, "Server misconfigured")
    if not hmac.compare_digest(x_admin_key, admin_key):
        raise HTTPException(403, "Forbidden")
