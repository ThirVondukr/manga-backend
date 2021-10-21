from typing import List, Dict
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.engine import Result

from db.dependencies import get_session
from db.models.manga.likes import MangaLike
from gql.users.context import get_current_user_from_context


async def user_liked_manga_count(user_ids: List[UUID]) -> List[int]:
    query = (
        select(MangaLike.user_id, func.count(MangaLike.user_id))
        .group_by(MangaLike.user_id)
        .filter(MangaLike.user_id.in_(user_ids))
    )
    async with get_session() as session:
        result: Result = await session.execute(query)

    results: Dict[UUID, int] = {user_id: likes_count for user_id, likes_count in result}
    return [results.get(user_id, 0) for user_id in user_ids]


async def manga_is_liked_by_viewer(manga_ids: List[UUID]) -> List[bool]:
    user = await get_current_user_from_context()
    if user is None:
        return [False for _ in manga_ids]

    query = select(MangaLike).filter(
        MangaLike.user_id == user.id, MangaLike.manga_id.in_(manga_ids)
    )
    async with get_session() as session:
        result: Result = await session.execute(query)

    liked_manga_ids = {like.manga_id for like in result.scalars()}
    return [manga_id in liked_manga_ids for manga_id in manga_ids]
