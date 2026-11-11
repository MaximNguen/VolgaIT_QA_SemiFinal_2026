from __future__ import annotations

from typing import Any, Dict, List, Mapping, Type, TypeVar
import logging
import allure
from pydantic import BaseModel, ConfigDict, Field, field_validator

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
    

class RegisterRequestSchema(SchemaModelMixin):
    """Схема для запроса на регистрацию"""
    model_config = ConfigDict(extra="allow", strict=True, populate_by_name=True)
    
    username: str = Field(..., description="Юзернейм пользователя для регистрации")
    password: str = Field(..., description="Пароль пользователя для регистрации")
    
class RegisterResponseSchema(SchemaModelMixin):
    """Схема для ответа регистрации пользователя"""
    
    