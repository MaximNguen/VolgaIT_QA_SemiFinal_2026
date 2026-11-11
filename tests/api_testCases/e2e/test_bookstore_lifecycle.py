import logging

import allure

from utils.api.payloads import (
    build_add_books_payload,
    build_delete_book_payload,
    build_user_payload,
)

logger = logging.getLogger(__name__)


@allure.epic("API - E2E Book Store")
@allure.feature("Жизненный цикл коллекции книг")
class TestBookStoreLifecycle:
    """E2E-сценарий: логин, магазин, добавление 3 книг, удаление 1."""

    @allure.title("Логин -> магазин -> добавить 3 книги -> удалить 1 -> профиль")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_bookstore_lifecycle(self, endpoint_factory):
        """Полный сценарий работы с коллекцией через API."""
        register = endpoint_factory.get("register")
        login = endpoint_factory.get("login")
        get_store_books = endpoint_factory.get("get_store_books")
        add_books = endpoint_factory.get("add_books")
        delete_book = endpoint_factory.get("delete_book")
        get_profile = endpoint_factory.get("get_profile_books")

        payload = build_user_payload()
        user = register.action(payload)
        token = login.action(payload).token
        assert token, "Не получен токен авторизации"

        store_books = get_store_books.action().books
        selected_isbns = [book.isbn for book in store_books[:3]]
        assert len(selected_isbns) == 3

        remaining_isbns = []
        try:
            added = add_books.action(
                build_add_books_payload(user.userID, selected_isbns),
                token,
            )
            assert [book.isbn for book in added.books] == selected_isbns

            profile_before = get_profile.action(user.userID, token)
            assert sorted(book.isbn for book in profile_before.books) == sorted(
                selected_isbns
            )

            deleted = delete_book.action(
                build_delete_book_payload(user.userID, selected_isbns[0]),
                token,
            )
            assert deleted is True

            profile_after = get_profile.action(user.userID, token)
            remaining_isbns = [book.isbn for book in profile_after.books]
            assert selected_isbns[0] not in remaining_isbns
            assert sorted(remaining_isbns) == sorted(selected_isbns[1:])
        finally:
            for isbn in selected_isbns[1:]:
                try:
                    delete_book.action(
                        build_delete_book_payload(user.userID, isbn),
                        token,
                    )
                except Exception as exc:
                    logger.warning(
                        f"Не удалось очистить книгу {isbn}: {exc}"
                    )
