from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.token import TokenPair, RefreshRequest, LogoutRequest
from app.schemas.user import UserCreate, UserRead
from app.services import auth as auth_service
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=201)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await auth_service.get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await auth_service.create_user(db, user_data)

@router.post("/login", response_model=TokenPair)
async def login(
    email: str,
    password: str,
    db: AsyncSession = Depends(get_db),
):
    user = await auth_service.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token, refresh_token, _ = await auth_service.create_token_pair(user)
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/refresh", response_model=TokenPair)
async def refresh_token(data: RefreshRequest):
    result = await auth_service.refresh_access_token(data.refresh_token)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    access_token, new_refresh_token, _ = result
    return {"access_token": access_token, "refresh_token": new_refresh_token}

@router.post("/logout")
async def logout(data: LogoutRequest):
    revoked = await auth_service.revoke_refresh_token(data.refresh_token)
    if not revoked:
        raise HTTPException(status_code=400, detail="Invalid refresh token")
    return {"message": "Successfully logged out"}