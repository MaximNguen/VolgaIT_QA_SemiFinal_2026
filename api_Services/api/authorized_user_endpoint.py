import logging
from typing import Any, Dict

import allure

from api_Services.api.base_endpoint import BaseEndpoint
from api_Services.schemas.base_schema import ErrorResponseSchema
from config import CHECKUSER_URL, TIMEOUT_SECONDS
from utils.api.api_validators import validate_login_request

logger = logging.getLogger(__name__)


class AuthorizedUserEndpoint(BaseEndpoint):
    """Эндпоинт проверки авторизации пользователя."""

    @allure.step("Проверяем авторизацию пользователя: {payload}")
    def action(self, payload: Dict[str, Any]) -> bool:
        """Проверяет, что пользователь авторизован."""
        validate_login_request(payload)
        logger.info(f"Проверяем авторизацию пользователя: {payload}")
        self.response = self.session.post(
            self.url(CHECKUSER_URL),
            json=payload,
            timeout=TIMEOUT_SECONDS,
        )
        self.check_status_code(200)
        self.response_json = self.response.json()
        return bool(self.response_json)

    @allure.step("Проверяем авторизацию с ошибкой, ожидаем {expected_code}")
    def action_expect_error(
        self,
        payload: Dict[str, Any],
        expected_code: int,
    ) -> ErrorResponseSchema:
        """Проверяет ответ проверки авторизации с ошибкой."""
        logger.info(f"Проверяем авторизацию с ожиданием ошибки: {payload}")
        self.response = self.session.post(
            self.url(CHECKUSER_URL),
            json=payload,
            timeout=TIMEOUT_SECONDS,
        )
        return self.parse_error_response(expected_code)
