from uuid import UUID

import strawberry


@strawberry.type(name="MangaArt")
class MangaArtType:
    id: UUID
    manga_id: UUID
    image_url: str
