import logging
from typing import Optional

import allure

from api_Services.api.base_endpoint import BaseEndpoint
from api_Services.schemas.UserSchema import ProfileResponseSchema
from api_Services.schemas.base_schema import ErrorResponseSchema
from config import TIMEOUT_SECONDS, USER_URL
from utils.api.api_validators import validate_profile_response

logger = logging.getLogger(__name__)


class GetProfileBooksEndpoint(BaseEndpoint):
    """Эндпоинт получения профиля пользователя с книгами."""

    @allure.step("Получаем профиль пользователя с ID: {user_id}")
    def action(self, user_id: str, token: str) -> ProfileResponseSchema:
        """Возвращает профиль пользователя и его книги."""
        logger.info(f"Получаем профиль пользователя с ID: {user_id}")
        self.response = self.session.get(
            self.url(f"{USER_URL}{user_id}"),
            headers=self.auth_headers(token),
            timeout=TIMEOUT_SECONDS,
        )
        self.check_status_code(200)
        self.response_json = self.response.json()
        return validate_profile_response(self.response_json)

    @allure.step("Получаем профиль с ошибкой, ожидаем {expected_code}")
    def action_expect_error(
        self,
        user_id: str,
        token: Optional[str],
        expected_code: int,
    ) -> ErrorResponseSchema:
        """Проверяет ответ получения профиля с ошибкой."""
        logger.info(f"Получаем профиль с ожиданием ошибки, ID: {user_id}")
        headers = self.auth_headers(token) if token else {}
        self.response = self.session.get(
            self.url(f"{USER_URL}{user_id}"),
            headers=headers,
            timeout=TIMEOUT_SECONDS,
        )
        return self.parse_error_response(expected_code)
