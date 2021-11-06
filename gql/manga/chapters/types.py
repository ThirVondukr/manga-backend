import datetime
from typing import Optional, List
from uuid import UUID

import strawberry
from strawberry import LazyType

from db.models.manga.chapters import MangaChapter
from gql.context import Info
from gql.manga.pages.types import MangaPageType
from gql.mixins import OrmTypeMixin
from . import _fields

MangaType = LazyType["MangaType", "gql.manga.manga.types"]


@strawberry.type(name="MangaChapter")
class MangaChapterType(OrmTypeMixin):
    id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    language: str
    number: int
    number_extra: Optional[int]
    title: Optional[str]
    published_at: datetime.datetime

    manga_id: UUID
    instance: strawberry.Private[MangaChapter]

    all_chapters = strawberry.field(_fields.all_chapters)
    previous = strawberry.field(_fields.previous)
    next = strawberry.field(_fields.next_)

    @strawberry.field
    async def manga(self, info: Info) -> MangaType:
        return await info.context.loaders.manga.load(self.manga_id)

    @strawberry.field
    async def pages(self, info: Info) -> List[MangaPageType]:
        pages = await info.context.loaders.chapter_pages.load(self.id)
        return [MangaPageType.from_orm(page) for page in pages]

    @classmethod
    def from_orm(cls, model: MangaChapter) -> "MangaChapterType":
        return cls(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            language=model.language,
            number=model.number,
            number_extra=model.number_extra,
            title=model.title,
            published_at=model.published_at,
            manga_id=model.manga_id,
            instance=model,
        )
