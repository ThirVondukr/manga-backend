import dataclasses
from typing import Optional, List, Union
from uuid import UUID

from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.dataloader import DataLoader
from strawberry.types import Info as StrawberryInfo

from db.models.manga import Manga, MangaPage, MangaInfo, MangaArt, Author


@dataclasses.dataclass
class Loaders:
    manga: DataLoader[UUID, Optional[Manga]]
    manga_infos: DataLoader[UUID, List[MangaInfo]]
    manga_arts: DataLoader[UUID, List[MangaArt]]
    manga_cover: DataLoader[UUID, Optional[MangaArt]]
    manga_likes_count: DataLoader[UUID, int]
    manga_artists: DataLoader[UUID, List[Author]]
    manga_writers: DataLoader[UUID, List[Author]]
    manga_is_liked_by_viewer: DataLoader[UUID, bool]
    user_liked_manga_count: DataLoader[UUID, int]
    chapter_pages: DataLoader[UUID, List[MangaPage]]


@dataclasses.dataclass
class Context:
    request: Union[Request, WebSocket]
    response: Optional[Response]
    loaders: Loaders


class Info(StrawberryInfo[Context, None]):
    pass
