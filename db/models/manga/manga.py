import uuid

from sqlalchemy import Column, String, select, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, column_property, Mapped

from db._mixins import DateTimeMixin
from db.base import Base
from db.models.manga import MangaChapter
from db.models.manga.art import MangaArt
from db.models.manga.info import MangaInfo
from db.models.manga.likes import MangaLike
from db.models.users import User


class Manga(Base, DateTimeMixin):
    __tablename__ = "manga__manga"

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    title: Mapped[str] = Column(String(255), nullable=False, unique=True)
    title_slug: Mapped[str] = Column(String(255), nullable=False, unique=True)

    infos = relationship(MangaInfo, uselist=True)
    arts = relationship(MangaArt, uselist=True)
    chapters: Mapped[MangaChapter] = relationship(
        "MangaChapter",
        back_populates="manga",
        uselist=True,
    )
    liked_by: Mapped[User] = relationship(
        "User",
        backref="liked_manga",
        secondary=MangaLike.__table__,
    )

    likes_count: Mapped[int] = column_property(
        select(func.count(MangaLike.manga_id))
        .filter(MangaLike.manga_id == id)
        .scalar_subquery(),
        deferred=True,
    )
