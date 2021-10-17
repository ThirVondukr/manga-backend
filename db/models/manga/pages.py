from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped

from db.base import Base

if TYPE_CHECKING:
    from db.models.manga import MangaChapter


class MangaPage(Base):
    __tablename__ = "manga__pages"

    id: Mapped[int] = Column(Integer, primary_key=True, nullable=False)
    number: Mapped[int] = Column(Integer, nullable=False)
    image_url: Mapped[str] = Column(String, nullable=False)

    chapter_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey("manga__chapters.id"), nullable=False
    )
    chapter: MangaChapter = relationship("MangaChapter", back_populates="pages")
