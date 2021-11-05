from collections import defaultdict
from typing import List, Iterable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db.dependencies import get_session
from db.models.manga import AuthorRelationship, AuthorRelationshipType, Author


def _make_load_fn(author_type: AuthorRelationshipType):
    async def load_fn(manga_ids: List[UUID]) -> List[List[Author]]:
        query = (
            select(AuthorRelationship)
            .options(joinedload(AuthorRelationship.author))
            .filter(
                AuthorRelationship.manga_id.in_(manga_ids),
                AuthorRelationship.type == author_type,
            )
        )
        async with get_session() as session:
            author_relationships: Iterable[AuthorRelationship] = await session.scalars(query)

        authors_by_manga_id: dict[UUID, list[Author]] = defaultdict(list)
        for ar in author_relationships:
            authors_by_manga_id[ar.manga_id].append(ar.author)

        return [authors_by_manga_id[manga_id] for manga_id in manga_ids]

    return load_fn


manga_artists = _make_load_fn(author_type=AuthorRelationshipType.artist)
manga_writers = _make_load_fn(author_type=AuthorRelationshipType.writer)
