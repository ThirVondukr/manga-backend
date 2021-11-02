from uuid import UUID

import strawberry

from db.models.manga import MangaPage


@strawberry.type
class MangaPageType:
    id: int
    number: int
    image_url: str
    chapter_id: UUID

    @classmethod
    def from_orm(cls, model: MangaPage):
        return cls(
            id=model.id,
            number=model.number,
            image_url=model.image_url,
            chapter_id=model.chapter_id,
        )
