from __future__ import annotations

from uuid import UUID

import strawberry

from db.models.manga import MangaArt
from gql.mixins import OrmTypeMixin


@strawberry.type(name="MangaArt")
class MangaArtType(OrmTypeMixin):
    id: UUID
    manga_id: UUID
    image_url: str

    @classmethod
    def from_orm(cls, model: MangaArt) -> MangaArtType:
        return cls(
            id=model.id,
            manga_id=model.manga_id,
            image_url=model.image_url,
        )
