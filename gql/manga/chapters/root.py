import strawberry

from . import resolvers


@strawberry.type
class ChaptersRoot:
    recent_chapters = strawberry.field(resolvers.resolve_latest_manga_chapters)
