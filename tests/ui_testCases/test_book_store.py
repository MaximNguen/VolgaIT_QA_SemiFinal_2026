import logging

import allure
import pytest

from data.ui_data.expected_data import (
    added_book,
    already_added,
    book_deleted,
    store_books,
)
from data.ui_data.urls import books_page_url, profile_page_url

logger = logging.getLogger(__name__)


@allure.epic("Book Store")
@allure.feature("Список книг магазина")
class TestBookStoreCatalog:
    """Тест-кейсы для получения списка книг магазина."""

    @allure.title("Список книг магазина содержит все ожидаемые книги")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_store_books_list(self, book_store_page):
        """Список книг магазина совпадает с ожидаемым."""
        book_store_page.open(books_page_url)
        assert book_store_page.check_store_loaded(), (
            "Страница магазина не загрузилась"
        )
        actual_books = sorted(
            (book["title"], book["author"], book["publisher"])
            for book in book_store_page.get_books()
        )
        assert actual_books == sorted(store_books), (
            "Список книг магазина не совпадает с ожидаемым"
        )


@allure.epic("Book Store")
@allure.feature("Коллекция книг пользователя")
class TestUserBookCollection:
    """Тест-кейсы для добавления, удаления и просмотра книг в профиле."""

    @pytest.fixture(autouse=True)
    def setup(self, empty_collection, book_store_page, profile_page):
        self.username, self.password = empty_collection
        self.book_store_page = book_store_page
        self.profile_page = profile_page

    def _add_books(self, titles):
        """Добавить книги в коллекцию через страницы магазина."""
        for title in titles:
            self.book_store_page.open(books_page_url)
            self.book_store_page.open_book(title)
            alert_text = self.book_store_page.add_book_to_collection()
            assert alert_text == added_book, (
                f"Книга '{title}' не добавлена в коллекцию: {alert_text}"
            )

    @allure.title("Добавление одной книги в коллекцию")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_one_book(self):
        """Одна добавленная книга отображается в профиле пользователя."""
        self.book_store_page.open(books_page_url)
        book = self.book_store_page.get_books()[0]
        self.book_store_page.open_book(book["title"])
        alert_text = self.book_store_page.add_book_to_collection()
        assert alert_text == added_book

        self.profile_page.open(profile_page_url)
        self.profile_page.wait_for_book(book["title"])
        assert self.profile_page.get_username() == self.username
        assert self.profile_page.get_books() == [book]

    @allure.title("Добавление нескольких книг в коллекцию")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_multiple_books(self):
        """Все добавленные книги отображаются в профиле пользователя."""
        self.book_store_page.open(books_page_url)
        books = self.book_store_page.get_books()[:3]
        self._add_books([book["title"] for book in books])

        self.profile_page.open(profile_page_url)
        for book in books:
            self.profile_page.wait_for_book(book["title"])
        profile_books = sorted(
            self.profile_page.get_books(), key=lambda item: item["title"]
        )
        expected_books = sorted(books, key=lambda item: item["title"])
        assert profile_books == expected_books

    @allure.title("Повторное добавление книги не дублирует её в профиле")
    def test_add_duplicate_book(self):
        """Повторное добавление книги показывает сообщение о дубликате."""
        self.book_store_page.open(books_page_url)
        title = self.book_store_page.get_book_titles()[0]
        self.book_store_page.open_book(title)
        assert self.book_store_page.add_book_to_collection() == added_book
        assert self.book_store_page.add_book_to_collection() == already_added

        self.profile_page.open(profile_page_url)
        self.profile_page.wait_for_book(title)
        assert self.profile_page.get_book_titles() == [title]

    @allure.title("Удаление одной книги из коллекции")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_one_book(self):
        """Удалённая книга исчезает из профиля, остальные остаются."""
        self.book_store_page.open(books_page_url)
        books = self.book_store_page.get_books()[:2]
        self._add_books([book["title"] for book in books])

        self.profile_page.open(profile_page_url)
        for book in books:
            self.profile_page.wait_for_book(book["title"])

        deleted_title, remaining_title = books[0]["title"], books[1]["title"]
        alert_text = self.profile_page.delete_book(deleted_title)
        assert alert_text == book_deleted
        assert self.profile_page.get_book_titles() == [remaining_title]

    @allure.title("Удаление нескольких книг из коллекции")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_multiple_books(self):
        """После удаления всех добавленных книг профиль пуст."""
        self.book_store_page.open(books_page_url)
        books = self.book_store_page.get_books()[:3]
        self._add_books([book["title"] for book in books])

        self.profile_page.open(profile_page_url)
        for book in books:
            self.profile_page.wait_for_book(book["title"])

        for book in books:
            alert_text = self.profile_page.delete_book(book["title"])
            assert alert_text == book_deleted, (
                f"Книга '{book['title']}' не удалена: {alert_text}"
            )
        assert self.profile_page.get_book_titles() == []
