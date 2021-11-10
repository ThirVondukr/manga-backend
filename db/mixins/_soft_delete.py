"""
Adapted example from sqlalchemy docs
https://docs.sqlalchemy.org/en/14/_modules/examples/extending_query/filter_public.html
"""

from sqlalchemy import Column, Boolean, event, orm, false
from sqlalchemy.orm import Mapped, Session, ORMExecuteState


class SoftDeleteMixin:
    is_deleted: Mapped[bool] = Column(Boolean, default=False, nullable=False)


@event.listens_for(Session, "do_orm_execute")
def _add_filtering_criteria(execute_state: ORMExecuteState):
    if (
        not execute_state.is_column_load
        and not execute_state.is_relationship_load
        and not execute_state.execution_options.get("include_deleted", False)
    ):
        execute_state.statement = execute_state.statement.options(
            orm.with_loader_criteria(
                SoftDeleteMixin,
                lambda cls: cls.is_deleted == false(),
                include_aliases=True,
            )
        )
