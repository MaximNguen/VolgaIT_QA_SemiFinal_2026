from __future__ import annotations

import logging
from typing import List, Optional

import allure
from pydantic import Field, ValidationInfo, field_validator

from api_Services.schemas.base_schema import SchemaModelMixin

logger = logging.getLogger(__name__)


class BookSchema(SchemaModelMixin):
    """Схема книги из Book Store."""

    isbn: str
    title: str
    subTitle: Optional[str] = None
    author: str
    publish_date: str
    publisher: str
    pages: int
    description: str
    website: Optional[str] = None

    @field_validator(
        "isbn",
        "title",
        "author",
        "publish_date",
        "publisher",
        "description",
    )
    @classmethod
    @allure.step("Проверка обязательных полей книги")
    def validate_required_fields(
        cls,
        v: str,
        info: ValidationInfo,
    ) -> str:
        if v.strip() != "":
            return v
        logger.error(f"Ошибка в ответе - пустое поле книги: {info.field_name}")
        raise ValueError(f"Ошибка поля книги: {info.field_name}")

    @field_validator("pages")
    @classmethod
    @allure.step("Проверка количества страниц книги")
    def validate_pages(cls, v: int) -> int:
        if v > 0:
            return v
        logger.error("Ошибка в ответе - невалидное количество страниц")
        raise ValueError("Ошибка pages")


class BooksResponseSchema(SchemaModelMixin):
    """Схема ответа со списком книг магазина."""

    books: List[BookSchema] = Field(default_factory=list)

    @field_validator("books")
    @classmethod
    @allure.step("Проверка, что список книг не пуст")
    def validate_books_not_empty(cls, v: List[BookSchema]) -> List[BookSchema]:
        if v:
            return v
        logger.error("Ошибка в ответе - пустой список книг")
        raise ValueError("Ошибка books")


class AddBookItemSchema(SchemaModelMixin):
    """Схема одной книги в запросе добавления в коллекцию."""

    isbn: str

    @field_validator("isbn")
    @classmethod
    @allure.step("Проверка валидности ISBN")
    def validate_isbn(cls, v: str) -> str:
        if v.strip() != "":
            return v
        logger.error("Ошибка в запросе - невалидный ISBN")
        raise ValueError("Ошибка ISBN")


class AddBooksRequestSchema(SchemaModelMixin):
    """Схема запроса добавления книг в коллекцию пользователя."""

    userId: str
    collectionOfIsbns: List[AddBookItemSchema]

    @field_validator("userId")
    @classmethod
    @allure.step("Проверка валидности userId")
    def validate_user_id(cls, v: str) -> str:
        if v.strip() != "":
            return v
        logger.error("Ошибка в запросе - невалидный userId")
        raise ValueError("Ошибка userId")

    @field_validator("collectionOfIsbns")
    @classmethod
    @allure.step("Проверка, что список ISBN не пуст")
    def validate_collection(
        cls,
        v: List[AddBookItemSchema],
    ) -> List[AddBookItemSchema]:
        if v:
            return v
        logger.error("Ошибка в запросе - пустой список ISBN")
        raise ValueError("Ошибка collectionOfIsbns")


class AddBooksResponseSchema(SchemaModelMixin):
    """Схема ответа добавления книг в коллекцию."""

    books: List[AddBookItemSchema] = Field(default_factory=list)

    @field_validator("books")
    @classmethod
    @allure.step("Проверка, что список добавленных книг не пуст")
    def validate_books_not_empty(
        cls,
        v: List[AddBookItemSchema],
    ) -> List[AddBookItemSchema]:
        if v:
            return v
        logger.error("Ошибка в ответе - пустой список добавленных книг")
        raise ValueError("Ошибка books")


class DeleteBookRequestSchema(SchemaModelMixin):
    """Схема запроса удаления книги из коллекции пользователя."""

    isbn: str
    userId: str

    @field_validator("isbn")
    @classmethod
    @allure.step("Проверка валидности ISBN")
    def validate_isbn(cls, v: str) -> str:
        if v.strip() != "":
            return v
        logger.error("Ошибка в запросе - невалидный ISBN")
        raise ValueError("Ошибка ISBN")

    @field_validator("userId")
    @classmethod
    @allure.step("Проверка валидности userId")
    def validate_user_id(cls, v: str) -> str:
        if v.strip() != "":
            return v
        logger.error("Ошибка в запросе - невалидный userId")
        raise ValueError("Ошибка userId")
