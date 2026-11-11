import logging

import allure

from data.ui_data.expected_data import added_book, book_deleted
from data.ui_data.urls import books_page_url, login_page_url, profile_page_url

logger = logging.getLogger(__name__)


@allure.epic("UI - E2E Book Store")
@allure.feature("Жизненный цикл коллекции книг")
class TestBookStoreFlow:
    """E2E-сценарий: логин, магазин, добавление 3 книг, удаление 1."""

    @allure.title("Логин -> магазин -> добавить 3 книги -> удалить 1 -> профиль")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_bookstore_flow(
        self,
        session_user,
        login_page,
        book_store_page,
        profile_page,
    ):
        """Полный сценарий работы с коллекцией через UI."""
        username, password = session_user

        login_page.open(login_page_url)
        login_page.login(username, password)
        login_page.wait_until_logged_in()

        profile_page.open(profile_page_url)
        for book in profile_page.get_books(load_timeout=2):
            profile_page.delete_book(book["title"])

        book_store_page.open(books_page_url)
        titles = [book["title"] for book in book_store_page.get_books()[:3]]
        assert len(titles) == 3

        for title in titles:
            book_store_page.open(books_page_url)
            book_store_page.open_book(title)
            alert_text = book_store_page.add_book_to_collection()
            assert alert_text == added_book, (
                f"Книга '{title}' не добавлена: {alert_text}"
            )

        profile_page.open(profile_page_url)
        for title in titles:
            profile_page.wait_for_book(title)
        assert sorted(profile_page.get_book_titles()) == sorted(titles)

        removed_title = titles[0]
        alert_text = profile_page.delete_book(removed_title)
        assert alert_text == book_deleted
        remaining_titles = profile_page.get_book_titles()
        assert sorted(remaining_titles) == sorted(titles[1:])

        for title in titles[1:]:
            profile_page.delete_book(title)
        assert profile_page.get_book_titles() == []
