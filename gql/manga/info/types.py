from uuid import UUID

import strawberry


@strawberry.type(name="MangaInfo")
class MangaInfoType:
    id: UUID
    lang: str
    title: str
    description: str
    manga_id: UUID
