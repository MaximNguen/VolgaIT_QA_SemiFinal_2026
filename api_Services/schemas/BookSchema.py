from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from api_Services.schemas.base_schema import SchemaModelMixin


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


class BooksResponseSchema(SchemaModelMixin):
    """Схема ответа со списком книг магазина."""

    books: List[BookSchema] = Field(default_factory=list)


class AddBookItemSchema(SchemaModelMixin):
    """Схема одной книги в запросе добавления в коллекцию."""

    isbn: str


class AddBooksRequestSchema(SchemaModelMixin):
    """Схема запроса добавления книг в коллекцию пользователя."""

    userId: str
    collectionOfIsbns: List[AddBookItemSchema]


class AddBooksResponseSchema(SchemaModelMixin):
    """Схема ответа добавления книг в коллекцию."""

    books: List[AddBookItemSchema] = Field(default_factory=list)


class DeleteBookRequestSchema(SchemaModelMixin):
    """Схема запроса удаления книги из коллекции пользователя."""

    isbn: str
    userId: str
