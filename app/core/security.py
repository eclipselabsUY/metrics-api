from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import secrets

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