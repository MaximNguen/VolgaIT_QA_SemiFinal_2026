import logging
from typing import Any, Dict

import allure

from api_Services.api.base_endpoint import BaseEndpoint
from api_Services.schemas.UserSchema import RegisterResponseSchema
from api_Services.schemas.base_schema import ErrorResponseSchema
from config import REGISTER_URL, TIMEOUT_SECONDS
from utils.api.api_validators import (
    validate_register_request,
    validate_register_response,
)

logger = logging.getLogger(__name__)


class RegisterUserEndpoint(BaseEndpoint):
    """Эндпоинт регистрации пользователя."""

    @allure.step("Регистрируем пользователя: {payload}")
    def action(self, payload: Dict[str, Any]) -> RegisterResponseSchema:
        """Регистрирует нового пользователя."""
        validate_register_request(payload)
        logger.info(f"Регистрируем пользователя: {payload}")
        self.response = self.session.post(
            self.url(REGISTER_URL),
            json=payload,
            timeout=TIMEOUT_SECONDS,
        )
        self.check_status_code(201)
        self.response_json = self.response.json()
        return validate_register_response(self.response_json)

    @allure.step("Регистрируем пользователя с ошибкой, ожидаем {expected_code}")
    def action_expect_error(
        self,
        payload: Dict[str, Any],
        expected_code: int,
    ) -> ErrorResponseSchema:
        """Пытается зарегистрировать пользователя и проверяет ошибку."""
        logger.info(f"Регистрируем пользователя с ожиданием ошибки: {payload}")
        self.response = self.session.post(
            self.url(REGISTER_URL),
            json=payload,
            timeout=TIMEOUT_SECONDS,
        )
        return self.parse_error_response(expected_code)
