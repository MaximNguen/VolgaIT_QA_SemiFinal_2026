import logging
from typing import Any, Dict

import allure

from api_Services.api.base_endpoint import BaseEndpoint
from api_Services.schemas.UserSchema import TokenResponseSchema
from api_Services.schemas.base_schema import ErrorResponseSchema
from config import LOGIN_URL, TIMEOUT_SECONDS
from utils.api.api_validators import (
    validate_login_request,
    validate_token_response,
)

logger = logging.getLogger(__name__)


class LoginUserEndpoint(BaseEndpoint):
    """Эндпоинт получения токена авторизации."""

    @allure.step("Получаем токен для пользователя: {payload}")
    def action(self, payload: Dict[str, Any]) -> TokenResponseSchema:
        """Авторизует пользователя и возвращает токен."""
        validate_login_request(payload)
        logger.info(f"Авторизуем пользователя: {payload}")
        self.response = self.session.post(
            self.url(LOGIN_URL),
            json=payload,
            timeout=TIMEOUT_SECONDS,
        )
        self.check_status_code(200)
        self.response_json = self.response.json()
        return validate_token_response(self.response_json)

    @allure.step("Авторизуемся с ошибкой, ожидаем {expected_code}")
    def action_expect_error(
        self,
        payload: Dict[str, Any],
        expected_code: int,
    ) -> ErrorResponseSchema:
        """Проверяет ответ авторизации с ошибкой."""
        logger.info(f"Авторизуемся с ожиданием ошибки: {payload}")
        self.response = self.session.post(
            self.url(LOGIN_URL),
            json=payload,
            timeout=TIMEOUT_SECONDS,
        )
        return self.parse_error_response(expected_code)
