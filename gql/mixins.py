from typing import Generic, TypeVar, List, Optional, Iterable

TModel = TypeVar("TModel")
TType = TypeVar("TType")


class OrmTypeMixin(Generic[TType, TModel]):
    @classmethod
    def from_orm(cls, model: TModel) -> TType:
        raise NotImplementedError

    @classmethod
    def from_orm_optional(cls, model: Optional[TModel]) -> Optional[TType]:
        if model is None:
            return None
        return cls.from_orm(model)

    @classmethod
    def from_orm_list(cls, models: Iterable[TModel]) -> List[TType]:
        return [cls.from_orm(model) for model in models]
