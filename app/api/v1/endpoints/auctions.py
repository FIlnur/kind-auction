import random

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models import Lot, User
from app.schemas.lot import (
    LotCreate,
    LotResponse,
    LotUpdate,
    UserContactsResponse,
    WishCreate,
    WishResponse,
)

router = APIRouter()


# Выложить лот

@router.post("/lots", response_model=LotResponse, status_code=status.HTTP_201_CREATED)
async def create_lot(
    lot_data: LotCreate, 
    db: AsyncSession = Depends(get_db) 
):
   
    new_lot = Lot(
        title=lot_data.title,
        image_url=lot_data.image_url,
        owner_id=lot_data.owner_id
    )
    db.add(new_lot)
    try:
        await db.commit()
        await db.refresh(new_lot)
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Ошибка создания лота.")
    return new_lot


# Удалить лот

@router.delete("/lots/{lot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lot(lot_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(delete(Lot).where(Lot.id == lot_id))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Лот не найден.")
    await db.commit()

# Обновить лот

@router.patch("/lots/{lot_id}", response_model=LotResponse)
async def update_lot(lot_id: int, lot_data: LotUpdate, db: AsyncSession = Depends(get_db)):
    update_data = lot_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления.")
    
    query = update(Lot).where(Lot.id == lot_id).values(**update_data).returning(Lot)
    result = await db.execute(query)
    lot = result.scalar_one_or_none()
    if not lot:
        raise HTTPException(status_code=404, detail="Лот не найден.")
    await db.commit()
    return lot

# Прочитать лот

@router.get("/lots/{lot_id}", response_model=LotResponse)
async def get_lot(lot_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lot).where(Lot.id == lot_id))
    lot = result.scalar_one_or_none()
    if not lot:
        raise HTTPException(status_code=404, detail="Лот не найден.")
    return lot

# Прочитать лоты с сортировкой по лайкам с подмешиванием случайных новых

@router.get("/lots", response_model=list[LotResponse])
async def get_sorted_lots(limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        popular_query = (
            select(Lot)
            .outerjoin(Lot.likers)  # Предполагается отношение likers в модели Lot
            .group_by(Lot.id)
            .order_by(func.count(User.id).desc())
            .limit(limit)
        )
        popular_res = await db.execute(popular_query)
        popular_lots = list(popular_res.scalars().all())
    except Exception:
        # Фолбэк, если отношения логов лайков еще нет в БД
        res = await db.execute(select(Lot).limit(limit))
        popular_lots = list(res.scalars().all())

    # 2. Получаем случайные новые лоты

    random_query = select(Lot).order_by(func.random()).limit(limit // 2)
    random_res = await db.execute(random_query)
    random_lots = random_res.scalars().all()

    # Смешиваем списки

    combined = list(set(popular_lots + list(random_lots)))
    random.shuffle(combined)
    return combined[:limit]

# Лайкнуть лот
@router.post("/lots/{lot_id}/like", status_code=status.HTTP_200_OK)
async def like_lot(lot_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    return {"status": "success", "detail": "Лот лайкнут"}

# Создать желание на получение лота

@router.post("/wishes", response_model=WishResponse)
async def create_wish(wish_data: WishCreate, db: AsyncSession = Depends(get_db)):
    return {"detail": "Желание создано"}

# Получить желания

@router.get("/wishes", response_model=list[WishResponse])
async def get_wishes(db: AsyncSession = Depends(get_db)):
    return []

# Удалить желание

@router.delete("/wishes/{wish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wish(wish_id: int, db: AsyncSession = Depends(get_db)):
    return

# Лайкнуть желание на получение лота

@router.post("/wishes/{wish_id}/like")
async def like_wish(wish_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    return {"status": "liked"}
# Убрать лайк на желании
@router.delete("/wishes/{wish_id}/like")
async def remove_wish_like(wish_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    return {"status": "unliked"}

# Выбрать победителя

@router.patch("/lots/{lot_id}/winner", response_model=LotResponse)
async def choose_winner(lot_id: int, winner_id: int, db: AsyncSession = Depends(get_db)):
    query = update(Lot).where(Lot.id == lot_id).values(winner_id=winner_id).returning(Lot)
    result = await db.execute(query)
    lot = result.scalar_one_or_none()
    if not lot:
        raise HTTPException(status_code=404, detail="Лот не найден.")
    await db.commit()
    return lot

# Получить контакты победителя

@router.get("/lots/{lot_id}/winner-contacts", response_model=UserContactsResponse)
async def get_winner_contacts(lot_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lot).where(Lot.id == lot_id).options(selectinload(Lot.winner)))
    lot = result.scalar_one_or_none()
    if not lot or not lot.winner:
        raise HTTPException(status_code=404, detail="Победитель или лот не найден.")
    return lot.winner

# Получить контакты хозяина лота

@router.get("/lots/{lot_id}/owner-contacts", response_model=UserContactsResponse)
async def get_owner_contacts(lot_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lot).where(Lot.id == lot_id).options(selectinload(Lot.owner)))
    lot = result.scalar_one_or_none()
    if not lot:
        raise HTTPException(status_code=404, detail="Лот не найден.")
    return lot.owner

# Получить выигранные лоты

@router.get("/users/{user_id}/won-lots", response_model=list[LotResponse])
async def get_won_lots(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lot).where(Lot.winner_id == user_id))
    return result.scalars().all()

# Подтвердить отправку лота

@router.post("/lots/{lot_id}/confirm-shipping")
async def confirm_shipping(lot_id: int, db: AsyncSession = Depends(get_db)):
    return {"status": "shipped", "lot_id": lot_id}

