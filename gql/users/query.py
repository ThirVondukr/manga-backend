import strawberry

from . import resolvers


@strawberry.type
class UsersQuery:
    viewer = strawberry.field(resolvers.get_viewer)
    get_user_by_id = strawberry.field(resolvers.get_user_by_id)
    get_user_by_username = strawberry.field(resolvers.get_user_by_username)
