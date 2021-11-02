import strawberry

from . import resolvers
from .permissions import IsAuthenticated


@strawberry.type
class UsersQuery:
    viewer = strawberry.field(resolvers.get_viewer, permission_classes=[IsAuthenticated])
    get_user_by_id = strawberry.field(resolvers.get_user_by_id)
    get_user_by_username = strawberry.field(resolvers.get_user_by_username)
