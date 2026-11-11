import logging

import allure

from api_Services.api.base_endpoint import BaseEndpoint
from api_Services.schemas.BookSchema import BooksResponseSchema
from config import GET_ALL_BOOKS_URL, TIMEOUT_SECONDS
from utils.api.api_validators import validate_books_response

logger = logging.getLogger(__name__)


class GetStoreBooksEndpoint(BaseEndpoint):
    """Эндпоинт получения списка книг магазина."""

    @allure.step("Получаем список книг магазина")
    def action(self) -> BooksResponseSchema:
        """Возвращает все книги магазина."""
        logger.info("Получаем список книг магазина")
        self.response = self.session.get(
            self.url(GET_ALL_BOOKS_URL),
            timeout=TIMEOUT_SECONDS,
        )
        self.check_status_code(200)
        self.response_json = self.response.json()
        return validate_books_response(self.response_json)
