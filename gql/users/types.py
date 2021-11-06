from __future__ import annotations

import math
from datetime import datetime
from typing import cast, Iterable, Optional
from uuid import UUID

import strawberry
from sqlalchemy import select, func

from db.dependencies import get_session
from db.models.manga import MangaLike, Manga
from db.models.users import User
from gql.context import Info
from gql.manga.chapters.resolvers import get_user_chapters_feed
from gql.manga.chapters.types import MangaChapterType
from gql.manga.manga.types import MangaType
from gql.mixins import OrmTypeMixin
from gql.pagination.types import (
    PaginationInput,
    PaginationInputPydantic,
    Connection,
    PagePagination,
    PagePaginationPageInfo,
)


@strawberry.type(name="User")
class UserType(OrmTypeMixin):
    id: UUID
    username: str
    avatar_url: str
    email: str
    joined_at: datetime

    @strawberry.field
    async def liked_manga_count(self, info: Info) -> int:
        return await info.context.loaders.user_liked_manga_count.load(self.id)

    @classmethod
    def from_orm(cls, user: User) -> UserType:
        return cls(
            id=user.id,
            username=user.username,
            avatar_url=user.avatar_url,
            email=user.email,
            joined_at=user.created_at,
        )

    @strawberry.field
    async def followed_manga(self, pagination: PaginationInput) -> PagePagination[MangaType]:
        pagination_pydantic: PaginationInputPydantic = pagination.to_pydantic()

        manga_query = (
            select(Manga).join(MangaLike).filter(MangaLike.user_id == self.id).order_by(Manga.title_slug)
        )
        likes_count_query = select(func.count(MangaLike.manga_id)).filter(MangaLike.user_id == self.id)
        manga_query = pagination_pydantic.apply_to_query(manga_query)
        async with get_session() as session:
            manga: Iterable[Manga] = (await session.scalars(manga_query)).unique()
            total_count: int = await session.scalar(likes_count_query)

        total_pages = math.ceil(total_count / pagination_pydantic.page_size)
        page_info = PagePaginationPageInfo(
            has_next=total_pages < pagination_pydantic.page,
            page=pagination_pydantic.page,
            page_size=pagination_pydantic.page_size,
            total_count=total_count,
            total_pages=total_pages,
        )
        return PagePagination(items=[MangaType.from_orm(m) for m in manga], page_info=page_info)

    @strawberry.field
    async def chapters_feed(
        self,
        first: int,
        after: Optional[datetime] = None,
    ) -> Connection[MangaChapterType]:
        return await get_user_chapters_feed(
            user=cast(User, self),
            first=first,
            after=after,
        )
