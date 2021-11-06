from operator import attrgetter
from typing import Optional
from uuid import UUID

from sqlalchemy import select

from db.models.manga.art import MangaArt
from gql.loaders import ModelListLoader, ModelLoader

manga_arts: ModelListLoader[UUID, MangaArt] = ModelListLoader(
    query=select(MangaArt),
    id_attr=MangaArt.manga_id,
    id_getter=attrgetter("manga_id")
)

manga_cover: ModelLoader[UUID, Optional[MangaArt]] = ModelLoader(
    query=select(MangaArt),
    id_attr=MangaArt.manga_id,
    id_getter=attrgetter("manga_id"),
)
