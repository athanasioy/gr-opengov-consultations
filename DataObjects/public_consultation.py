from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date,datetime

from DataObjects.base import Base


class PublicConsultation(Base):
    __tablename__ = "PublicConsultation"

    id: Mapped[int] = mapped_column(primary_key=True)
    reporter: Mapped[str] = mapped_column(String(100))
    text: Mapped[str] = mapped_column(String)
    date_reported: Mapped[datetime] = mapped_column()
    url: Mapped[str] = mapped_column(String(1000))
    article_id: Mapped[int] = mapped_column(ForeignKey("Article.id"))
    articles: Mapped["Article"] = relationship(back_populates="public_consultations")

