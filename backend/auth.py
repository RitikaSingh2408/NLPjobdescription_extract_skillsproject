import os
import base64
import hashlib
import hmac
import jwt

from datetime import datetime, timedelta, timezone


SECRET_KEY = os.getenv(
    "JOB_SKILL_SECRET_KEY",
    "change-this-secret-key-before-production"
)

ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000
    )

    return (
        base64.b64encode(salt).decode("utf-8")
        + "$"
        + base64.b64encode(password_hash).decode("utf-8")
    )


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt_b64, hash_b64 = stored_hash.split("$")

        salt = base64.b64decode(salt_b64)
        stored_password_hash = base64.b64decode(hash_b64)

        new_password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            600_000
        )

        return hmac.compare_digest(
            new_password_hash,
            stored_password_hash
        )

    except Exception:
        return False


def create_access_token(user_id: int, username: str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload
    except jwt.PyJWTError:
        return None