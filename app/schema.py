from pydantic import BaseModel


def _snake_to_camel(name: str) -> str:
    parts = name.split("_")
    for i, part in enumerate(parts[1:], start=1):
        parts[i] = part.capitalize()
    return "".join(parts)


class SchemaBase(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = _snake_to_camel
