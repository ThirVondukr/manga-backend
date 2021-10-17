from typing import Protocol, TypeVar, Type, Generic, Sequence, Callable

from .types import Connection, PageInfo, Edge

TModel = TypeVar("TModel", contravariant=True)
TType = TypeVar("TType", covariant=True)


class FromORM(Protocol[TModel, TType]):
    @classmethod
    def from_orm(cls, model: TModel) -> TType:
        ...


class CursorPaginator(Generic[TModel, TType]):
    def __init__(
        self,
        type_cls: Type[FromORM[TModel, TType]],
        cursor_func: Callable[[TType], str]
    ):
        self.type_cls = type_cls
        self.cursor_func = cursor_func

    def parse_sequence(self, sequence: Sequence[TModel], first: int) -> Connection[TType]:
        if not sequence:
            return Connection(
                page_info=PageInfo(end_cursor="", has_next_page=False),
                edges=[],
            )

        has_next_page = len(sequence) > first
        sequence = sequence[:first]
        nodes = [self.type_cls.from_orm(model=model) for model in sequence]

        page_info = PageInfo(
            has_next_page=has_next_page,
            end_cursor=self.cursor_func(nodes[-1])
        )
        edges = [Edge(node=node, cursor=self.cursor_func(node)) for node in nodes]
        return Connection(edges=edges, page_info=page_info)
