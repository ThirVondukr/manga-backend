import enum
import uuid

from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped

from db.base import Base


class AuthorRelationshipType(enum.Enum):
    writer = "writer"
    artist = "artist"


class Author(Base):
    __tablename__ = "manga__author"

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True), default=uuid.uuid4, nullable=False, primary_key=True
    )
    name: Mapped[str] = Column(String, nullable=False)


class AuthorRelationship(Base):
    __tablename__ = "manga__manga_authors"

    author_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        ForeignKey("manga__author.id"),
        nullable=False,
        primary_key=True,
    )
    author: Author = relationship("Author")
    manga_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        ForeignKey("manga__manga.id"),
        nullable=False,
        primary_key=True,
    )
    type: AuthorRelationshipType = Column(
        Enum(AuthorRelationshipType), nullable=False, primary_key=True
    )
