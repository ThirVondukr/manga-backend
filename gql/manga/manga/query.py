import strawberry

from . import resolvers


@strawberry.type
class MangaQuery:
    get_manga_by_id = strawberry.field(resolvers.get_manga_by_id)
    get_manga_by_title_slug = strawberry.field(resolvers.get_manga_by_title_slug)

    search_manga = strawberry.field(resolvers.search_manga)
    popular_manga = strawberry.field(resolvers.popular_manga)
