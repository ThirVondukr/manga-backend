from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped

from db.base import Base

if TYPE_CHECKING:
    from db.models.manga import Manga


class MangaArt(Base):
    __tablename__ = "manga__manga_art"
    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )

    manga_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        ForeignKey("manga__manga.id"),
        nullable=False,
    )
    image_url: Mapped[str] = Column(String(length=255), nullable=False)
    manga: Mapped[Manga] = relationship("Manga", back_populates="arts")
