from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped

from db import _fields
from db.base import Base

if TYPE_CHECKING:
    from db.models.manga import Manga


class MangaInfo(Base):
    __tablename__ = "manga__manga_info"

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )

    lang: Mapped[str] = Column(String(length=2), nullable=False)
    title: Mapped[str] = Column(String(length=255), nullable=False)
    description: Mapped[str] = Column(String(length=2047), nullable=True)

    manga_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        ForeignKey("manga__manga.id"),
        nullable=False,
    )
    manga: Mapped[Manga] = relationship("Manga", back_populates="infos")
