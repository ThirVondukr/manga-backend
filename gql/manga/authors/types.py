from uuid import UUID

import strawberry

from db.models.manga import Author
from gql.mixins import OrmTypeMixin


@strawberry.type(name="Author")
class AuthorType(OrmTypeMixin):
    id: UUID
    name: str

    @classmethod
    def from_orm(cls, author: Author):
        return cls(
            id=author.id,
            name=author.name,
        )
