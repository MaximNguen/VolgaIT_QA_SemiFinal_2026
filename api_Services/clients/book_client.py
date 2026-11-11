import logging
from typing import List, Optional

import allure

from api_Services.clients.baseClient import BaseClient
from api_Services.schemas.BookSchema import (
    AddBooksResponseSchema,
    BookSchema,
    BooksResponseSchema,
)
from api_Services.schemas.UserSchema import ProfileResponseSchema
from api_Services.schemas.base_schema import ErrorResponseSchema
from config import ADD_BOOKS_URL, DELETE_BOOK_URL, GET_ALL_BOOKS_URL, USER_URL
from data.api_data.http_method_enum import HTTPMethod
from utils.api.api_validators import (
    validate_add_books_request,
    validate_add_books_response,
    validate_books_response,
    validate_delete_book_request,
    validate_error_response,
    validate_profile_response,
)

logger = logging.getLogger(__name__)


class BookClient(BaseClient):
    """Клиент для работы с Book Store API."""

    @allure.step("Получаем список книг магазина")
    def get_store_books(self) -> BooksResponseSchema:
        """Возвращает список книг магазина."""
        logger.info("Получаем список книг магазина")
        response = self.send_request(HTTPMethod.GET, GET_ALL_BOOKS_URL)
        self.check_status_code(response, 200)
        return validate_books_response(response.json())

    @allure.step("Ищем книгу по ISBN: {isbn}")
    def get_store_book_by_isbn(self, isbn: str) -> Optional[BookSchema]:
        """Возвращает книгу магазина по ISBN, если она существует."""
        books = self.get_store_books().books
        return next((book for book in books if book.isbn == isbn), None)

    @allure.step("Добавляем книги в коллекцию: {payload}")
    def add_books(
        self,
        payload: dict,
        token: str,
    ) -> AddBooksResponseSchema:
        """Добавляет книги в коллекцию пользователя."""
        validate_add_books_request(payload)
        logger.info(f"Добавляем книги в коллекцию: {payload}")
        response = self.send_request(
            HTTPMethod.POST,
            ADD_BOOKS_URL,
            json=payload,
            headers=self.auth_headers(token),
        )
        self.check_status_code(response, 201)
        return validate_add_books_response(response.json())

    @allure.step("Добавляем книги с ошибкой, ожидаем {expected_code}")
    def add_books_expect_error(
        self,
        payload: dict,
        token: Optional[str],
        expected_code: int,
    ) -> ErrorResponseSchema:
        """Проверяет добавление книг с ожидаемой ошибкой."""
        response = self.send_request(
            HTTPMethod.POST,
            ADD_BOOKS_URL,
            json=payload,
            headers=self.auth_headers(token),
        )
        self.check_status_code(response, expected_code)
        return validate_error_response(response.json())

    @allure.step("Удаляем книгу из коллекции: {payload}")
    def delete_book(self, payload: dict, token: str) -> bool:
        """Удаляет книгу из коллекции пользователя."""
        validate_delete_book_request(payload)
        logger.info(f"Удаляем книгу из коллекции: {payload}")
        response = self.send_request(
            HTTPMethod.DELETE,
            DELETE_BOOK_URL,
            json=payload,
            headers=self.auth_headers(token),
        )
        self.check_status_code(response, 204)
        return True

    @allure.step("Удаляем книгу с ошибкой, ожидаем {expected_code}")
    def delete_book_expect_error(
        self,
        payload: dict,
        token: Optional[str],
        expected_code: int,
    ) -> ErrorResponseSchema:
        """Проверяет удаление книги с ожидаемой ошибкой."""
        response = self.send_request(
            HTTPMethod.DELETE,
            DELETE_BOOK_URL,
            json=payload,
            headers=self.auth_headers(token),
        )
        self.check_status_code(response, expected_code)
        return validate_error_response(response.json())

    @allure.step("Получаем книги профиля пользователя: {user_id}")
    def get_profile_books(
        self,
        user_id: str,
        token: str,
    ) -> ProfileResponseSchema:
        """Возвращает профиль пользователя с книгами."""
        logger.info(f"Получаем книги профиля пользователя: {user_id}")
        response = self.send_request(
            HTTPMethod.GET,
            f"{USER_URL}{user_id}",
            headers=self.auth_headers(token),
        )
        self.check_status_code(response, 200)
        return validate_profile_response(response.json())

    @allure.step("Получаем профиль с ошибкой, ожидаем {expected_code}")
    def get_profile_books_expect_error(
        self,
        user_id: str,
        token: Optional[str],
        expected_code: int,
    ) -> ErrorResponseSchema:
        """Проверяет получение профиля с ожидаемой ошибкой."""
        response = self.send_request(
            HTTPMethod.GET,
            f"{USER_URL}{user_id}",
            headers=self.auth_headers(token),
        )
        self.check_status_code(response, expected_code)
        return validate_error_response(response.json())

    @allure.step("Удаляем все книги из коллекции пользователя: {user_id}")
    def delete_all_books(self, user_id: str, token: str) -> int:
        """Удаляет все книги из коллекции и возвращает их количество."""
        books: List[BookSchema] = self.get_profile_books(user_id, token).books
        deleted = 0
        for book in books:
            payload = {"isbn": book.isbn, "userId": user_id}
            response = self.send_request(
                HTTPMethod.DELETE,
                DELETE_BOOK_URL,
                json=payload,
                headers=self.auth_headers(token),
            )
            if response.status_code == 204:
                deleted += 1
        logger.info(f"Удалено книг из коллекции: {deleted}")
        return deleted
