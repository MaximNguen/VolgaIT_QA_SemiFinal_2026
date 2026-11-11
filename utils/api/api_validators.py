import logging
from typing import Any, Mapping, Type, TypeVar

import allure
from pydantic import BaseModel, ValidationError

from api_Services.schemas.BookSchema import (
    AddBooksRequestSchema,
    AddBooksResponseSchema,
    BooksResponseSchema,
    DeleteBookRequestSchema,
)
from api_Services.schemas.UserSchema import (
    LoginRequestSchema,
    ProfileResponseSchema,
    RegisterRequestSchema,
    RegisterResponseSchema,
    TokenResponseSchema,
)
from api_Services.schemas.base_schema import ErrorResponseSchema

logger = logging.getLogger(__name__)

TSchema = TypeVar("TSchema", bound=BaseModel)


def _validate(
    schema: Type[TSchema],
    response_json: Mapping[str, Any],
    description: str,
) -> TSchema:
    """Проверяет, что данные соответствуют pydantic-схеме."""
    with allure.step(description):
        logger.info(f"{description}. Данные: {response_json}")
        try:
            return schema.from_dict(response_json)
        except ValidationError as exc:
            logger.error(f"Ошибка валидации схемы {schema.__name__}: {exc}")
            raise ValueError(
                f"Ответ не соответствует схеме {schema.__name__}: {exc}"
            ) from exc


def validate_register_request(
    payload: Mapping[str, Any],
) -> RegisterRequestSchema:
    """Проверяет запрос регистрации пользователя."""
    return _validate(
        RegisterRequestSchema,
        payload,
        "Проверяем запрос регистрации пользователя",
    )


def validate_register_response(
    response_json: Mapping[str, Any],
) -> RegisterResponseSchema:
    """Проверяет ответ регистрации пользователя."""
    return _validate(
        RegisterResponseSchema,
        response_json,
        "Проверяем ответ регистрации пользователя",
    )


def validate_login_request(payload: Mapping[str, Any]) -> LoginRequestSchema:
    """Проверяет запрос авторизации пользователя."""
    return _validate(
        LoginRequestSchema,
        payload,
        "Проверяем запрос авторизации пользователя",
    )


def validate_token_response(
    response_json: Mapping[str, Any],
) -> TokenResponseSchema:
    """Проверяет ответ генерации токена."""
    return _validate(
        TokenResponseSchema,
        response_json,
        "Проверяем ответ генерации токена",
    )


def validate_books_response(
    response_json: Mapping[str, Any],
) -> BooksResponseSchema:
    """Проверяет ответ со списком книг магазина."""
    return _validate(
        BooksResponseSchema,
        response_json,
        "Проверяем ответ со списком книг магазина",
    )


def validate_profile_response(
    response_json: Mapping[str, Any],
) -> ProfileResponseSchema:
    """Проверяет ответ профиля пользователя."""
    return _validate(
        ProfileResponseSchema,
        response_json,
        "Проверяем ответ профиля пользователя",
    )


def validate_add_books_request(
    payload: Mapping[str, Any],
) -> AddBooksRequestSchema:
    """Проверяет запрос добавления книг в коллекцию."""
    return _validate(
        AddBooksRequestSchema,
        payload,
        "Проверяем запрос добавления книг в коллекцию",
    )


def validate_add_books_response(
    response_json: Mapping[str, Any],
) -> AddBooksResponseSchema:
    """Проверяет ответ добавления книг в коллекцию."""
    return _validate(
        AddBooksResponseSchema,
        response_json,
        "Проверяем ответ добавления книг в коллекцию",
    )


def validate_delete_book_request(
    payload: Mapping[str, Any],
) -> DeleteBookRequestSchema:
    """Проверяет запрос удаления книги из коллекции."""
    return _validate(
        DeleteBookRequestSchema,
        payload,
        "Проверяем запрос удаления книги из коллекции",
    )


def validate_error_response(
    response_json: Mapping[str, Any],
) -> ErrorResponseSchema:
    """Проверяет ответ API с ошибкой."""
    return _validate(
        ErrorResponseSchema,
        response_json,
        "Проверяем ответ API с ошибкой",
    )
