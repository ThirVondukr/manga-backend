import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped

from db.base import Base


class MangaLike(Base):
    __tablename__ = "manga__manga_likes"

    user_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey("users__users.id"), primary_key=True
    )
    manga_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), ForeignKey("manga__manga.id"), primary_key=True
    )
