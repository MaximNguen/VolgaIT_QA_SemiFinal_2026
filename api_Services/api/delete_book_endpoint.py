import logging
from typing import Any, Dict, Optional

import allure

from api_Services.api.base_endpoint import BaseEndpoint
from api_Services.schemas.base_schema import ErrorResponseSchema
from config import DELETE_BOOK_URL, TIMEOUT_SECONDS
from utils.api.api_validators import validate_delete_book_request

logger = logging.getLogger(__name__)


class DeleteBookEndpoint(BaseEndpoint):
    """Эндпоинт удаления книги из коллекции пользователя."""

    @allure.step("Удаляем книгу из коллекции: {payload}")
    def action(self, payload: Dict[str, Any], token: str) -> bool:
        """Удаляет книгу из коллекции пользователя."""
        validate_delete_book_request(payload)
        logger.info(f"Удаляем книгу из коллекции: {payload}")
        self.response = self.session.delete(
            self.url(DELETE_BOOK_URL),
            json=payload,
            headers=self.auth_headers(token),
            timeout=TIMEOUT_SECONDS,
        )
        self.check_status_code(204)
        return True

    @allure.step("Удаляем книгу с ошибкой, ожидаем {expected_code}")
    def action_expect_error(
        self,
        payload: Dict[str, Any],
        token: Optional[str],
        expected_code: int,
    ) -> ErrorResponseSchema:
        """Проверяет ответ удаления книги с ошибкой."""
        logger.info(f"Удаляем книгу с ожиданием ошибки: {payload}")
        headers = self.auth_headers(token) if token else {}
        self.response = self.session.delete(
            self.url(DELETE_BOOK_URL),
            json=payload,
            headers=headers,
            timeout=TIMEOUT_SECONDS,
        )
        return self.parse_error_response(expected_code)
