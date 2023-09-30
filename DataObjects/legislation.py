from typing import Optional, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import date
from sqlalchemy import String
from DataObjects.base import Base


class Legislation(Base):
    __tablename__ = "Legislation"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    ministry: Mapped[Optional[str]] = mapped_column(String(100))
    date_posted: Mapped[Optional[date]] = mapped_column()
    parliament_url: Mapped[Optional[str]] = mapped_column(String(1000))
    legislation_pdf_url: Mapped[Optional[str]] = mapped_column(String(1000))
    scrap_url: Mapped[Optional[str]] = mapped_column(String(1000))
    final_legislation_id: Mapped[int] = mapped_column(ForeignKey("Legislation.id"), nullable=True)
    final_legislation: Mapped["Legislation"] = relationship(back_populates="public_consultations",remote_side=[id])  # Remote side is the master row
    public_consultations: Mapped["Legislation"] = relationship(back_populates="final_legislation")

    articles: Mapped[List["Article"]] = relationship(back_populates="legislation")
    fek_number: Mapped[Optional[str]] = mapped_column(String(100))
    legislation_type: Mapped[Optional[str]] = mapped_column(String(100))

    def __repr__(self) ->str:
        return f"Legislation(id={self.id}, title={self.title}, ministry={self.ministry}, date_posted={self.date_posted})"
