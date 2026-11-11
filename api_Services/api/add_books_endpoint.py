import logging
from typing import Any, Dict, Optional

import allure

from api_Services.api.base_endpoint import BaseEndpoint
from api_Services.schemas.BookSchema import AddBooksResponseSchema
from api_Services.schemas.base_schema import ErrorResponseSchema
from config import ADD_BOOKS_URL, TIMEOUT_SECONDS
from utils.api.api_validators import (
    validate_add_books_request,
    validate_add_books_response,
)

logger = logging.getLogger(__name__)


class AddBooksEndpoint(BaseEndpoint):
    """Эндпоинт добавления книг в коллекцию пользователя."""

    @allure.step("Добавляем книги в коллекцию: {payload}")
    def action(
        self,
        payload: Dict[str, Any],
        token: str,
    ) -> AddBooksResponseSchema:
        """Добавляет книги в коллекцию пользователя."""
        validate_add_books_request(payload)
        logger.info(f"Добавляем книги в коллекцию: {payload}")
        self.response = self.session.post(
            self.url(ADD_BOOKS_URL),
            json=payload,
            headers=self.auth_headers(token),
            timeout=TIMEOUT_SECONDS,
        )
        self.check_status_code(201)
        self.response_json = self.response.json()
        return validate_add_books_response(self.response_json)

    @allure.step("Добавляем книги с ошибкой, ожидаем {expected_code}")
    def action_expect_error(
        self,
        payload: Dict[str, Any],
        token: Optional[str],
        expected_code: int,
    ) -> ErrorResponseSchema:
        """Проверяет ответ добавления книг с ошибкой."""
        logger.info(f"Добавляем книги с ожиданием ошибки: {payload}")
        headers = self.auth_headers(token) if token else {}
        self.response = self.session.post(
            self.url(ADD_BOOKS_URL),
            json=payload,
            headers=headers,
            timeout=TIMEOUT_SECONDS,
        )
        return self.parse_error_response(expected_code)
