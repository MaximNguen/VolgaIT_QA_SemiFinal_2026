import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import allure
import requests

from api_Services.schemas.base_schema import ErrorResponseSchema
from config import BASE_URL, HEADERS
from utils.api.api_validators import validate_error_response

logger = logging.getLogger(__name__)


class BaseEndpoint(ABC):
    """
    Базовый класс для всех API-эндпоинтов.
    Содержит общие методы для отправки HTTP-запросов и обработки ответов.
    """

    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = (base_url or BASE_URL).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.response: Optional[requests.Response] = None
        self.response_json: Optional[Dict[str, Any]] = None

    def url(self, path: str) -> str:
        """Собирает полный URL эндпоинта."""
        return f"{self.base_url}{path}"

    @staticmethod
    def auth_headers(token: str) -> Dict[str, str]:
        """Возвращает заголовок авторизации с Bearer-токеном."""
        return {"Authorization": f"Bearer {token}"}

    @abstractmethod
    def action(self, *args, **kwargs) -> Any:
        """Основное действие эндпоинта."""

    @allure.step("Проверяем, что код статуса - {expected_code}")
    def check_status_code(self, expected_code: int) -> None:
        """Проверяет статус-код последнего ответа."""
        logger.info(f"Проверяем, что код статуса - {expected_code}")
        assert self.response is not None, "Ответ ещё не получен"
        actual_code = self.response.status_code
        assert actual_code == expected_code, (
            f"Ожидали {expected_code}, получили {actual_code}. "
            f"Ответ: {self.response.text}"
        )

    @allure.step("Разбираем ответ с ошибкой, ожидаем код {expected_code}")
    def parse_error_response(
        self,
        expected_code: int,
    ) -> ErrorResponseSchema:
        """Проверяет статус-код ошибки и валидирует тело ответа."""
        self.check_status_code(expected_code)
        self.response_json = self.response.json() if self.response.text else {}
        return validate_error_response(self.response_json)
