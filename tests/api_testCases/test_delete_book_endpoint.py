import logging

import allure

from utils.api.payloads import (
    build_add_books_payload,
    build_delete_book_payload,
)

logger = logging.getLogger(__name__)


@allure.epic("API - Book Store")
@allure.feature("Удаление книги из коллекции")
class TestDeleteBookEndpoint:
    """Тесты удаления книг из коллекции пользователя."""

    @allure.title("Удаление одной книги из коллекции")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_one_book(
        self,
        book_client,
        api_user,
        store_books,
        api_clean_books,
    ):
        """Удалённая книга исчезает из профиля, остальные остаются."""
        isbns = [book.isbn for book in store_books[:2]]
        added = build_add_books_payload(api_user["userId"], isbns)
        book_client.add_books(added, api_user["token"])

        payload = build_delete_book_payload(api_user["userId"], isbns[0])
        result = book_client.delete_book(payload, api_user["token"])
        profile = book_client.get_profile_books(
            api_user["userId"],
            api_user["token"],
        )

        assert result is True
        assert [book.isbn for book in profile.books] == [isbns[1]]

    @allure.title("Удаление книги, которой нет в коллекции")
    def test_delete_book_not_in_collection(
        self,
        book_client,
        api_user,
        store_books,
    ):
        """Удаление отсутствующей книги возвращает код 1206."""
        payload = build_delete_book_payload(
            api_user["userId"],
            store_books[0].isbn,
        )

        error = book_client.delete_book_expect_error(
            payload,
            api_user["token"],
            expected_code=400,
        )

        assert error.code == "1206"
        assert "not available" in error.message.lower()

    @allure.title("Удаление книги без токена авторизации")
    def test_delete_book_without_token(
        self,
        book_client,
        api_user,
        store_books,
        api_clean_books,
    ):
        """Запрос без токена возвращает 401."""
        isbn = store_books[0].isbn
        added = build_add_books_payload(api_user["userId"], [isbn])
        book_client.add_books(added, api_user["token"])

        payload = build_delete_book_payload(api_user["userId"], isbn)
        error = book_client.delete_book_expect_error(
            payload,
            token=None,
            expected_code=401,
        )

        assert error.code == "1200"
        assert error.message == "User not authorized!"
