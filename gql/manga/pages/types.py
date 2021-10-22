from uuid import UUID

import strawberry


@strawberry.type
class MangaPageType:
    id: int
    image_url: str
    chapter_id: UUID
