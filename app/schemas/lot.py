from typing import Optional

from pydantic import BaseModel


class LotCreate(BaseModel):
    title: str
    image_url: str
    owner_id: int

class LotUpdate(BaseModel):
    title: Optional[str] = None
    image_url: Optional[str] = None

class LotResponse(BaseModel):
    id: int
    title: str
    image_url: str
    owner_id: int
    winner_id: Optional[int] = None

    class Config:
        from_attributes = True

class UserContactsResponse(BaseModel):
    id: int
    email: str

class WishCreate(BaseModel):
    user_id: int
    lot_id: int

class WishResponse(BaseModel):
    id: int
    user_id: int
    lot_id: int

    class Config:
        from_attributes = True