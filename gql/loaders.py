import collections
from operator import attrgetter
from typing import TypeVar, Generic, Callable, Iterable, Optional

from mypy.api import List
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import Select

from db.dependencies import get_session

TId = TypeVar("TId")
TModel = TypeVar("TModel")

IdGetter = Callable[[TModel], TId]
ModelGetter = Callable[..., TModel]


class Loader(Generic[TId, TModel]):
    id_getter: IdGetter = attrgetter("id")
    model_getter: ModelGetter = lambda obj: obj

    def __init__(
        self,
        query: Select,
        id_attr: Mapped[TId],
        id_getter=id_getter,
        model_getter=model_getter,
    ):
        self.query = query
        self.id_attr = id_attr
        self.id_getter = id_getter
        self.model_getter = model_getter


class ModelLoader(Loader, Generic[TId, TModel]):
    def __init__(self, *args, **kwargs):
        self.default = kwargs.pop("default", None)
        super().__init__(*args, **kwargs)

    async def __call__(self, keys: List[TId]) -> List[TModel]:
        query = self.query.filter(self.id_attr.in_(keys))
        async with get_session() as session:
            scalars: Iterable[TModel] = await session.scalars(query)

        scalars_by_key = {self.id_getter(s): self.model_getter(s) for s in scalars}
        return [scalars_by_key.get(key, self.default) for key in keys]


class ModelListLoader(Loader, Generic[TId, TModel]):
    async def __call__(self, keys: List[TId]) -> List[List[TModel]]:
        query = self.query.filter(self.id_attr.in_(keys))
        async with get_session() as session:
            scalars: Iterable[TModel] = await session.scalars(query)

        scalars_by_key: dict[TId, List[TModel]] = collections.defaultdict(list)
        for scalar in scalars:
            scalars_by_key[self.id_getter(scalar)].append(self.model_getter(scalar))

        return [scalars_by_key.get(key, []) for key in keys]
