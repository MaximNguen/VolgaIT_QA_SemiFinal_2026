import logging

import allure

from utils.api.payloads import build_add_books_payload

logger = logging.getLogger(__name__)


@allure.epic("API - Account")
@allure.feature("Профиль пользователя")
class TestProfileBooksEndpoint:
    """Тесты получения списка книг из профиля."""

    @allure.title("Получение профиля с добавленными книгами")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_profile_books(
        self,
        book_client,
        api_user,
        store_books,
        api_clean_books,
    ):
        """Профиль возвращает пользователя и его книги."""
        isbns = [book.isbn for book in store_books[:3]]
        payload = build_add_books_payload(api_user["userId"], isbns)
        book_client.add_books(payload, api_user["token"])

        profile = book_client.get_profile_books(
            api_user["userId"],
            api_user["token"],
        )

        assert profile.userId == api_user["userId"]
        assert profile.username == api_user["username"]
        assert sorted(book.isbn for book in profile.books) == sorted(isbns)

    @allure.title("Получение профиля без токена авторизации")
    def test_get_profile_without_token(self, book_client, api_user):
        """Запрос профиля без токена возвращает 401."""
        error = book_client.get_profile_books_expect_error(
            api_user["userId"],
            token=None,
            expected_code=401,
        )

        assert error.code == "1200"
        assert error.message == "User not authorized!"
