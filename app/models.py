from typing import List, Optional

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[str] = mapped_column(default="user")

    lots: Mapped[List["Lot"]] = relationship(
        back_populates="owner", 
        foreign_keys="[Lot.owner_id]"
    )
    winned_lots: Mapped[List["Lot"]] = relationship(
        back_populates="winner", 
        foreign_keys="[Lot.winner_id]"
    )


class Lot(Base):
    __tablename__= "lots"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICTED"))
    winner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="RESTRICTED"))

    owner: Mapped["User"] = relationship(
        back_populates="lots", 
        foreign_keys=[owner_id]
    )

    winner: Mapped[Optional["User"]] = relationship(
        back_populates="winned_lots", 
        foreign_keys=[winner_id]
    )