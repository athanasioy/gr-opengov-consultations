from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from DataObjects.base import Base
from typing import List, Optional

class Article(Base):
    __tablename__ = "Article"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(String)
    title: Mapped[str] = mapped_column(String(200))
    text: Mapped[str] = mapped_column(String)
    legislation_id: Mapped[int] = mapped_column(ForeignKey("Legislation.id"))
    comments_allowed: Mapped[Optional[bool]] = mapped_column(default=True) 
    article_url: Mapped[Optional[str]] = mapped_column()

    legislation: Mapped["Legislation"] = relationship(back_populates="articles")
    public_consultations: Mapped[List["PublicConsultation"]] = relationship(back_populates="articles")
