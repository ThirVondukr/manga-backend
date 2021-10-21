from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped

from db._mixins import DateTimeMixin
from db.base import Base

if TYPE_CHECKING:
    from db.models.manga import Manga, MangaPage


class MangaChapter(Base, DateTimeMixin):
    __tablename__ = "manga__chapters"
    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )

    language: Mapped[str] = Column(String(length=2), nullable=False)
    number: Mapped[str] = Column(String(length=255), nullable=False)
    title: Mapped[Optional[str]] = Column(String(length=255), nullable=True)
    published_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)

    manga_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey("manga__manga.id"), nullable=False
    )
    manga: Mapped[Manga] = relationship("Manga", back_populates="chapters")
    pages: Mapped[MangaPage] = relationship("MangaPage", back_populates="chapter")
