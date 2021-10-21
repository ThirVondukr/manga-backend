import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Column
from sqlalchemy.dialects.postgresql import UUID


def utcnow():
    return datetime.now(tz=timezone.utc)


LANGUAGE_STR = String(length=2)
UUID_PK = Column(
    UUID(as_uuid=True),
    default=uuid.uuid4,
    primary_key=True,
    nullable=False,
)
