from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from data_objects.base import Base
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
    voted_article_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Article.id"))

    legislation: Mapped["Legislation"] = relationship(back_populates="articles")
    public_consultations: Mapped[List["PublicConsultation"]] = relationship(back_populates="articles")
    voted_article: Mapped["Article"] = relationship(back_populates="proposed_article", remote_side=[id]) 
    proposed_article: Mapped[List["Article"]] = relationship(back_populates="voted_article")

    def __repr__(self) -> str:
        return f"Article(id={self.id}, number={self.number}, title={self.title}, text={self.text[:50]}, legislation_id={self.legislation_id})"

class ArticleSimilarity(Base):
    __tablename__= "ArticleSimilarity"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    p_articleID: Mapped[int] = mapped_column(ForeignKey("Article.id"))
    f_articleID: Mapped[int] = mapped_column(ForeignKey("Article.id"))
    similarity: Mapped[float] = mapped_column()
    method: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"ArticleSimilarity(id={self.id}, p_articleID={self.p_articleID}, f_articleID={self.f_articleID})"