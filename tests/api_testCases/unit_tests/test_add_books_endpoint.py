import logging

import allure

from utils.api.payloads import (
    build_add_books_payload,
    get_invalid_isbn,
)

logger = logging.getLogger(__name__)


@allure.epic("API - Book Store")
@allure.feature("Добавление книг в коллекцию")
class TestAddBooksEndpoint:
    """Тесты добавления книг в коллекцию пользователя."""

    @allure.title("Добавление одной книги в коллекцию")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_one_book(self, book_client, api_user, store_books, api_clean_books):
        """Книга добавляется и отображается в профиле."""
        isbn = store_books[0].isbn
        payload = build_add_books_payload(api_user["userId"], [isbn])

        added = book_client.add_books(payload, api_user["token"])
        profile = book_client.get_profile_books(
            api_user["userId"],
            api_user["token"],
        )

        assert [book.isbn for book in added.books] == [isbn]
        assert isbn in [book.isbn for book in profile.books]

    @allure.title("Добавление нескольких книг в коллекцию")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_multiple_books(
        self,
        book_client,
        api_user,
        store_books,
        api_clean_books,
    ):
        """Все выбранные книги добавляются в коллекцию."""
        isbns = [book.isbn for book in store_books[:3]]
        payload = build_add_books_payload(api_user["userId"], isbns)

        added = book_client.add_books(payload, api_user["token"])
        profile = book_client.get_profile_books(
            api_user["userId"],
            api_user["token"],
        )

        assert [book.isbn for book in added.books] == isbns
        assert sorted(book.isbn for book in profile.books) == sorted(isbns)

    @allure.title("Повторное добавление книги отклоняется")
    def test_add_duplicate_book(
        self,
        book_client,
        api_user,
        store_books,
        api_clean_books,
    ):
        """Повторное добавление возвращает код 1210."""
        isbn = store_books[0].isbn
        payload = build_add_books_payload(api_user["userId"], [isbn])
        book_client.add_books(payload, api_user["token"])

        error = book_client.add_books_expect_error(
            payload,
            api_user["token"],
            expected_code=400,
        )

        assert error.code == "1210"
        assert "already present" in error.message.lower()

    @allure.title("Добавление книги с несуществующим ISBN")
    def test_add_invalid_isbn(self, book_client, api_user, api_clean_books):
        """Несуществующий ISBN возвращает код 1205."""
        payload = build_add_books_payload(
            api_user["userId"],
            [get_invalid_isbn()],
        )

        error = book_client.add_books_expect_error(
            payload,
            api_user["token"],
            expected_code=400,
        )

        assert error.code == "1205"
        assert "not available" in error.message.lower()

    @allure.title("Добавление книги без токена авторизации")
    def test_add_books_without_token(
        self,
        book_client,
        api_user,
        store_books,
        api_clean_books,
    ):
        """Запрос без токена возвращает 401."""
        payload = build_add_books_payload(
            api_user["userId"],
            [store_books[0].isbn],
        )

        error = book_client.add_books_expect_error(
            payload,
            token=None,
            expected_code=401,
        )

        assert error.code == "1200"
        assert error.message == "User not authorized!"
