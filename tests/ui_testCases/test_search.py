import logging

import allure
import pytest

from data.ui_data.expected_data import search_cases, search_no_results
from data.ui_data.urls import books_page_url

logger = logging.getLogger(__name__)


@allure.epic("Страница магазина (Поисковик)")
@allure.feature("Проверка функционала поисковика")
class TestSearchFunction:
    """Тест-кейсы для поиска книг в магазине."""

    @pytest.fixture(autouse=True)
    def setup(self, book_store_page):
        self.book_store_page = book_store_page

    @allure.title("Поиск книг по валидному тексту: {text}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "text, expected_titles",
        search_cases,
        ids=["Git", "git", "JavaScript"],
    )
    def test_valid_text_search(self, text, expected_titles):
        """Поиск возвращает только книги, содержащие запрос."""
        self.book_store_page.open(books_page_url)
        assert self.book_store_page.check_search_input()
        self.book_store_page.search_books(text)

        actual_titles = self.book_store_page.get_search_result_titles()
        assert actual_titles == expected_titles, (
            f"Для запроса '{text}' ожидали {expected_titles}, "
            f"получили {actual_titles}"
        )

    @allure.title("Поиск книг без результатов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_without_results(self):
        """Несуществующий запрос скрывает все книги."""
        self.book_store_page.open(books_page_url)
        self.book_store_page.search_books(search_no_results)

        assert self.book_store_page.get_search_result_titles() == []
