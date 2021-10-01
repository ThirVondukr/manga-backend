from datetime import datetime, timezone

from sqlalchemy import String


def utcnow():
    return datetime.now(tz=timezone.utc)


LANGUAGE_STR = String(length=2)
