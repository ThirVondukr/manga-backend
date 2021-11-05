from operator import attrgetter

from sqlalchemy import select

from db.models.manga.art import MangaArt
from gql.loaders import ModelListLoader, ModelLoader

manga_arts = ModelListLoader(
    query=select(MangaArt),
    id_attr=MangaArt.manga_id,
    id_getter=attrgetter("manga_id")
)

manga_cover = ModelLoader(
    query=select(MangaArt),
    id_attr=MangaArt.manga_id,
    id_getter=attrgetter("manga_id")
)
