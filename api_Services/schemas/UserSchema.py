from __future__ import annotations

import logging
from typing import List, Optional

import allure
from pydantic import Field, field_validator

from api_Services.schemas.base_schema import SchemaModelMixin
from api_Services.schemas.BookSchema import BookSchema

logger = logging.getLogger(__name__)


class RegisterRequestSchema(SchemaModelMixin):
    """Схема запроса регистрации пользователя."""

    userName: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

    @field_validator("userName")
    @classmethod
    @allure.step("Проверка валидности никнейма")
    def validate_user_name(cls, v: str) -> str:
        if v.strip() != "":
            return v
        logger.error("Ошибка в запросе - невалидный username")
        raise ValueError("Ошибка username")

    @field_validator("password")
    @classmethod
    @allure.step("Проверка валидности пароля")
    def validate_password(cls, v: str) -> str:
        if len(v.strip()) >= 8:
            return v
        logger.error("Ошибка в запросе - невалидный password")
        raise ValueError("Ошибка password")


class RegisterResponseSchema(SchemaModelMixin):
    """Схема ответа успешной регистрации пользователя."""

    userID: str
    username: str
    books: List[BookSchema] = Field(default_factory=list)

    @field_validator("userID")
    @classmethod
    @allure.step("Проверка валидности userID")
    def validate_user_id(cls, v: str) -> str:
        if v.strip() != "":
            return v
        logger.error("Ошибка в ответе - невалидный userID")
        raise ValueError("Ошибка userID")

    @field_validator("username")
    @classmethod
    @allure.step("Проверка валидности никнейма")
    def validate_user_name(cls, v: str) -> str:
        if v.strip() != "":
            return v
        logger.error("Ошибка в ответе - невалидный username")
        raise ValueError("Ошибка username")


class LoginRequestSchema(SchemaModelMixin):
    """Схема запроса авторизации пользователя."""

    userName: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

    @field_validator("userName")
    @classmethod
    @allure.step("Проверка валидности никнейма")
    def validate_user_name(cls, v: str) -> str:
        if v.strip() != "":
            return v
        logger.error("Ошибка в запросе - невалидный username")
        raise ValueError("Ошибка username")

    @field_validator("password")
    @classmethod
    @allure.step("Проверка валидности пароля")
    def validate_password(cls, v: str) -> str:
        if v.strip() != "":
            return v
        logger.error("Ошибка в запросе - невалидный password")
        raise ValueError("Ошибка password")


class TokenResponseSchema(SchemaModelMixin):
    """Схема ответа генерации токена."""

    token: Optional[str] = None
    expires: Optional[str] = None
    status: str
    result: str

    @field_validator("status")
    @classmethod
    @allure.step("Проверка валидности статуса токена")
    def validate_status(cls, v: str) -> str:
        if v.strip() != "":
            return v
        logger.error("Ошибка в ответе - невалидный status")
        raise ValueError("Ошибка status")

    @field_validator("result")
    @classmethod
    @allure.step("Проверка валидности результата токена")
    def validate_result(cls, v: str) -> str:
        if v.strip() != "":
            return v
        logger.error("Ошибка в ответе - невалидный result")
        raise ValueError("Ошибка result")


class ProfileResponseSchema(SchemaModelMixin):
    """Схема ответа профиля пользователя."""

    userId: str
    username: str
    books: List[BookSchema] = Field(default_factory=list)

    @field_validator("userId")
    @classmethod
    @allure.step("Проверка валидности userId")
    def validate_user_id(cls, v: str) -> str:
        if v.strip() != "":
            return v
        logger.error("Ошибка в ответе - невалидный userId")
        raise ValueError("Ошибка userId")

    @field_validator("username")
    @classmethod
    @allure.step("Проверка валидности никнейма")
    def validate_user_name(cls, v: str) -> str:
        if v.strip() != "":
            return v
        logger.error("Ошибка в ответе - невалидный username")
        raise ValueError("Ошибка username")
