from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property

from db._fields import utcnow
from db.base import Base


class User(Base):
    __tablename__ = "users__users"

    id: uuid.UUID = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    created_at: datetime = Column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False,
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )

    username: str = Column(String, nullable=False, unique=True)
    password_hash: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False)

    @hybrid_property
    def avatar_url(self):
        return f"user-avatars/{self.id}.png"
