from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
import uuid

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_token(subject: str, token_type: str, expires_delta: timedelta, jti: Optional[str] = None) -> str:
    now = datetime.now(timezone.utc)
    expire = now + expires_delta
    payload = {
        "sub": subject,
        "type": token_type,
        "exp": expire,
        "iat": now,
    }
    if jti:
        payload["jti"] = jti
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def create_access_token(user_id: int) -> str:
    expire = timedelta(minutes=settings.access_token_expire_minutes)
    return create_token(str(user_id), "access", expire)

def create_refresh_token(user_id: int) -> str:
    expire = timedelta(days=settings.refresh_token_expire_days)
    jti = str(uuid.uuid4())
    token = create_token(str(user_id), "refresh", expire, jti)
    return token, jti

def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None