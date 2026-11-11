from __future__ import annotations

from typing import Any, Dict, Mapping, Type, TypeVar

from pydantic import BaseModel

TModel = TypeVar("TModel", bound="SchemaModelMixin")


class SchemaModelMixin(BaseModel):
    """Базовый миксин для явной сериализации/десериализации моделей."""

    @classmethod
    def from_dict(cls: Type[TModel], data: Mapping[str, Any]) -> TModel:
        return cls.model_validate(dict(data))

    @classmethod
    def from_json(cls: Type[TModel], data: str | bytes | bytearray) -> TModel:
        return cls.model_validate_json(data)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(mode="python")

    def to_json(self) -> str:
        return self.model_dump_json()


class ErrorResponseSchema(SchemaModelMixin):
    """Схема ответа API с ошибкой."""

    code: str
    message: str
