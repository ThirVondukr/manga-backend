from collections import defaultdict
from typing import List, Iterable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import Select

from db.dependencies import get_session
from db.models.manga import AuthorRelationship, AuthorRelationshipType
from gql.manga.authors.types import AuthorType


def _get_authors_query(manga_ids: List[UUID], type_: AuthorRelationshipType) -> Select:
    return (
        select(AuthorRelationship)
        .options(joinedload(AuthorRelationship.author))
        .filter(
            AuthorRelationship.manga_id.in_(manga_ids),
            AuthorRelationship.type == type_,
        )
    )


def _make_load_fn(author_type: AuthorRelationshipType):
    async def load_fn(manga_ids: List[UUID]) -> List[List[AuthorType]]:
        query = _get_authors_query(manga_ids, type_=author_type)
        async with get_session() as session:
            author_relationships_result = await session.execute(query)
        author_relationships: Iterable[AuthorRelationship] = author_relationships_result.scalars()
        author_relationships_by_manga_id: dict[UUID, list[AuthorType]] = defaultdict(list)
        for ar in author_relationships:
            author_relationships_by_manga_id[ar.manga_id].append(AuthorType.from_orm(ar.author))

        return [author_relationships_by_manga_id[manga_id] for manga_id in manga_ids]

    return load_fn


manga_artists = _make_load_fn(author_type=AuthorRelationshipType.artist)
manga_writers = _make_load_fn(author_type=AuthorRelationshipType.writer)
