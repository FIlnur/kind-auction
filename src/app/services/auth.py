import json
from datetime import timedelta
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.user import User
from app.schemas.user import UserCreate
from app.db.redis import redis_client
from app.core.config import settings

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    hashed_password = get_password_hash(user_data.password)
    db_user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

async def create_token_pair(user: User) -> tuple[str, str, str]:
    access_token = create_access_token(user.id)
    refresh_token, jti = create_refresh_token(user.id)
    # Сохраняем refresh token в Redis
    expire_seconds = settings.refresh_token_expire_days * 24 * 3600
    await redis_client.setex(
        f"refresh_token:{jti}",
        expire_seconds,
        json.dumps({"user_id": user.id})
    )
    return access_token, refresh_token, jti

async def refresh_access_token(refresh_token: str) -> Optional[tuple[str, str, str]]:
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        return None
    jti = payload.get("jti")
    if not jti:
        return None

    # Проверяем наличие токена в Redis
    stored = await redis_client.get(f"refresh_token:{jti}")
    if not stored:
        return None

    # Удаляем старый токен (ротация)
    await redis_client.delete(f"refresh_token:{jti}")

    # Создаём новую пару
    user_id = int(payload["sub"])
    access_token = create_access_token(user_id)
    new_refresh_token, new_jti = create_refresh_token(user_id)
    expire_seconds = settings.refresh_token_expire_days * 24 * 3600
    await redis_client.setex(
        f"refresh_token:{new_jti}",
        expire_seconds,
        json.dumps({"user_id": user_id})
    )
    return access_token, new_refresh_token, new_jti

async def revoke_refresh_token(refresh_token: str) -> bool:
    payload = decode_token(refresh_token)
    if not payload:
        return False
    jti = payload.get("jti")
    if not jti:
        return False
    await redis_client.delete(f"refresh_token:{jti}")
    return True