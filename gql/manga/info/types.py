from uuid import UUID

import strawberry

from db.models.manga import MangaInfo
from gql.mixins import OrmTypeMixin


@strawberry.type(name="MangaInfo")
class MangaInfoType(OrmTypeMixin):
    id: UUID
    lang: str
    title: str
    description: str
    manga_id: UUID

    @classmethod
    def from_orm(cls, model: MangaInfo):
        return cls(
            id=model.id,
            lang=model.lang,
            title=model.title,
            description=model.description,
            manga_id=model.manga_id,
        )
