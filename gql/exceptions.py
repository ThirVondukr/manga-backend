import uuid

import strawberry


@strawberry.type
class NotAuthenticated:
    @strawberry.field
    def message(self) -> str:
        return "You must be authenticated to perform this operation"


@strawberry.type
class NotFound:
    entity_id: uuid.UUID
    message: str
