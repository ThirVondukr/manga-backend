import strawberry

from . import resolvers


@strawberry.type
class ChaptersQuery:
    recent_chapters = strawberry.field(resolvers.resolve_latest_manga_chapters)
    get_chapter_by_id = strawberry.field(resolvers.get_chapter_by_id)
