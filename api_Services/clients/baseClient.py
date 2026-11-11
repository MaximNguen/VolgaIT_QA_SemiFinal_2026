import logging
from typing import Any, Dict, Optional

import allure
import requests

from config import BASE_URL, HEADERS, TIMEOUT_SECONDS
from data.api_data.http_method_enum import HTTPMethod

logger = logging.getLogger(__name__)


class BaseClient:
    """
    Базовый клиент для взаимодействия с API.
    Содержит общие методы для отправки HTTP-запросов и обработки ответов.
    """

    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout: int = TIMEOUT_SECONDS,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    @staticmethod
    def auth_headers(token: Optional[str] = None) -> Dict[str, str]:
        """Возвращает заголовок авторизации, если передан токен."""
        return {"Authorization": f"Bearer {token}"} if token else {}

    @staticmethod
    def check_status_code(
        response: requests.Response,
        expected_code: int,
    ) -> None:
        """Проверяет статус-код ответа."""
        assert response.status_code == expected_code, (
            f"Ожидали {expected_code}, получили {response.status_code}. "
            f"Ответ: {response.text}"
        )

    def send_request(
        self,
        method: HTTPMethod,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """Отправляет запрос и возвращает ответ."""
        url = f"{self.base_url}{path}"
        with allure.step(
            f"Отправляем {method.value} запрос на URL: {url} с данными: {json}"
        ):
            logger.info(
                f"Отправляем {method.value} запрос на URL: {url} с данными: {json}"
            )
            try:
                return self.session.request(
                    method=method.value,
                    url=url,
                    json=json,
                    headers=headers,
                    timeout=self.timeout,
                )
            except requests.exceptions.RequestException as exc:
                logger.error(f"Ошибка при отправке запроса: {exc}")
                raise
