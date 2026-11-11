import logging

import allure

logger = logging.getLogger(__name__)


@allure.epic("API - Book Store")
@allure.feature("Список книг магазина")
class TestStoreBooksEndpoint:
    """Тесты получения списка книг магазина."""

    @allure.title("Получение списка книг магазина")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_store_books(self, book_client):
        """API возвращает все книги каталога с полными данными."""
        response = book_client.get_store_books()
        isbns = [book.isbn for book in response.books]

        assert len(response.books) == 8
        assert len(set(isbns)) == len(isbns), "ISBN книг должны быть уникальны"
        assert "9781449325862" in isbns

        book = next(item for item in response.books if item.isbn == "9781449325862")
        assert book.title == "Git Pocket Guide"
        assert book.author == "Richard E. Silverman"
        assert book.publisher == "O'Reilly Media"
