from datetime import datetime
from typing import cast, Iterable, Optional
from uuid import UUID

import strawberry
from sqlalchemy import select
from strawberry.types import Info

from db.dependencies import get_session
from db.models.manga import MangaLike, Manga
from db.models.users import User
from gql.manga.chapters.resolvers import get_user_chapters_feed
from gql.manga.chapters.types import LatestMangaChapters
from gql.manga.manga.types import MangaType
from gql.pagination.types import PaginationInput, PaginationPydantic
from gql.users.loaders import MangaLoaders


@strawberry.type(name="User")
class UserType:
    id: UUID
    username: str
    avatar_url: str
    email: str
    joined_at: datetime

    @strawberry.field
    def liked_manga_count(self, info: Info) -> int:
        return cast(
            int, info.context[MangaLoaders.user_liked_manga_count].load(self.id)
        )

    @classmethod
    def from_orm(cls, user: User) -> "UserType":
        return cls(
            id=user.id,
            username=user.username,
            avatar_url=user.avatar_url,
            email=user.email,
            joined_at=user.created_at,
        )

    @classmethod
    def maybe_from_orm(cls, user: Optional[User]) -> Optional["UserType"]:
        if user is None:
            return None
        return cls.from_orm(user)

    @strawberry.field
    async def followed_manga(self, pagination: PaginationInput) -> list[MangaType]:
        pagination_pydantic: PaginationPydantic = pagination.to_pydantic()

        query = (
            select(Manga)
            .join(MangaLike)
            .filter(MangaLike.user_id == self.id)
            .order_by(Manga.title_slug)
        )
        query = pagination_pydantic.apply_to_query(query)
        async with get_session() as session:
            result = await session.execute(query)
        manga: Iterable[Manga] = result.scalars().unique()
        return [MangaType.from_orm(m) for m in manga]

    @strawberry.field
    async def chapters_feed(
        self,
        first: int,
        after: Optional[datetime] = None,
    ) -> LatestMangaChapters:
        return await get_user_chapters_feed(
            user=cast(User, self),
            first=first,
            after=after,
        )
