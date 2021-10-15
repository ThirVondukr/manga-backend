from __future__ import annotations

from typing import TypeVar, Generic, List

import strawberry
from pydantic import BaseModel, conint
from sqlalchemy.sql import Select

TNode = TypeVar("TNode")


@strawberry.type
class PagePagination(Generic[TNode]):
    page_info: PagePaginationPageInfo
    items: List[TNode]


@strawberry.type
class PagePaginationPageInfo:
    has_next: bool
    page: int
    page_size: int
    total_count: int
    total_pages: int


class PaginationInputPydantic(BaseModel):
    page: conint(ge=1) = 1
    page_size: conint(ge=1, le=100) = 10

    def apply_to_query(self, query: Select) -> Select:
        return query.limit(self.page_size).offset((self.page - 1) * self.page_size)


@strawberry.experimental.pydantic.input(
    model=PaginationInputPydantic,
    fields=["page", "page_size"],
    name="Pagination",
)
class PaginationInput:
    pass


@strawberry.type
class Edge(Generic[TNode]):
    node: TNode
    cursor: str


@strawberry.type
class PageInfo:
    end_cursor: str
    has_next_page: bool


@strawberry.type
class Connection(Generic[TNode]):
    edges: List[Edge]
    page_info: PageInfo
