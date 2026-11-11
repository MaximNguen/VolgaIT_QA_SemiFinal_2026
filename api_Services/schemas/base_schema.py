from __future__ import annotations

import logging
from typing import Any, Dict, Mapping, Type, TypeVar

import allure
from pydantic import BaseModel, field_validator

logger = logging.getLogger(__name__)

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

    @field_validator("code", "message")
    @classmethod
    @allure.step("Проверка полей ответа с ошибкой")
    def validate_error_fields(cls, v: str) -> str:
        if v.strip() != "":
            return v
        logger.error("Ошибка в ответе - пустое поле ошибки")
        raise ValueError("Ошибка полей ответа с ошибкой")
