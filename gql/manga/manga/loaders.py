from operator import attrgetter
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import load_only

from db.models.manga import Manga
from gql.loaders import ModelLoader

load_manga: ModelLoader[UUID, Manga] = ModelLoader(
    select(Manga),
    id_attr=Manga.id,
)

manga_likes: ModelLoader[UUID, int] = ModelLoader(
    query=select(Manga).options(load_only(Manga.id, Manga.likes_count)),
    id_attr=Manga.id,
    model_getter=attrgetter("likes_count"),
    default=0,
)
