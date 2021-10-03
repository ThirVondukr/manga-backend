from typing import TypeVar, Generic, List

import strawberry
from pydantic import BaseModel, conint
from sqlalchemy.sql import Select


@strawberry.type
class PagePaginationPageInfo:
    has_next: bool
    page: int
    page_size: int
    total_count: int
    total_pages: int


class PaginationPydantic(BaseModel):
    page: conint(ge=1) = 1
    page_size: conint(ge=1, le=100) = 10

    def apply_to_query(self, query: Select) -> Select:
        return query.limit(self.page_size).offset((self.page - 1) * self.page_size)


@strawberry.experimental.pydantic.input(
    model=PaginationPydantic,
    fields=["page", "page_size"],
    name="Pagination",
)
class PaginationInput:
    pass


Node = TypeVar("Node")
Cursor = TypeVar("Cursor")


@strawberry.type
class Edge(Generic[Node, Cursor]):
    node: Node
    cursor: Cursor


@strawberry.type
class PageInfo(Generic[Cursor]):
    end_cursor: Cursor
    has_next_page: bool


@strawberry.type
class Connection(Generic[Node, Cursor]):
    edges: List[Edge]
    page_info: PageInfo
