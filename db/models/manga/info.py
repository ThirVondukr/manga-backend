from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped

from db import _fields
from db._mixins import UUIDMixin
from db.base import Base

if TYPE_CHECKING:
    from db.models.manga import Manga


class MangaInfo(Base, UUIDMixin):
    __tablename__ = "manga__manga_info"

    lang = Column(_fields.LANGUAGE_STR, nullable=False)
    title = Column(String(length=255), nullable=False)
    description = Column(String(length=2047), nullable=True)

    manga_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        ForeignKey("manga__manga.id"),
        nullable=False,
    )
    manga: Mapped[Manga] = relationship("Manga", back_populates="infos")
