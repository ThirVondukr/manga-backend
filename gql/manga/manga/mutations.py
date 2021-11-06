from uuid import UUID

import strawberry
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from strawberry.types import Info

from db.dependencies import get_session
from db.models.manga import Manga, MangaLike
from gql.exceptions import NotAuthenticated, NotFound
from gql.manga.manga.types import MangaType
from gql.users.permissions import IsAuthenticated


@strawberry.type
class LikeMangaSuccess:
    manga: MangaType = strawberry.field()


LikeMangaResponse = strawberry.union(
    "LikeMangaResponse",
    (NotFound, NotAuthenticated, LikeMangaSuccess),
)


@strawberry.type
class MangaMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def set_manga_liked(
        self,
        info: Info,
        manga_id: UUID,
        liked: bool = True,
    ) -> LikeMangaResponse:
        user = await info.context.user()
        if user is None:
            return NotAuthenticated()

        query = select(Manga).filter(Manga.id == manga_id).limit(1)
        async with get_session() as session:
            manga = (await session.execute(query)).scalar_one_or_none()
            if manga is None:
                return NotFound(
                    entity_id=manga_id,
                    message=f"Manga with id {manga_id} not found",
                )
            if liked:
                stmt = (
                    insert(MangaLike)
                    .values(user_id=user.id, manga_id=manga_id)
                    .on_conflict_do_nothing()
                )
            else:
                stmt = delete(MangaLike).filter(
                    MangaLike.manga_id == manga_id, MangaLike.user_id == user.id
                )
            await session.execute(stmt)
            await session.commit()
            await session.refresh(manga)

        return LikeMangaSuccess(manga=manga)
