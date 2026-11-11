import logging

import allure

from api_Services.clients.baseClient import BaseClient
from api_Services.schemas.UserSchema import (
    ProfileResponseSchema,
    RegisterResponseSchema,
    TokenResponseSchema,
)
from api_Services.schemas.base_schema import ErrorResponseSchema
from config import CHECKUSER_URL, LOGIN_URL, REGISTER_URL, USER_URL
from data.api_data.http_method_enum import HTTPMethod
from utils.api.api_validators import (
    validate_error_response,
    validate_login_request,
    validate_profile_response,
    validate_register_request,
    validate_register_response,
    validate_token_response,
)

logger = logging.getLogger(__name__)


class UserClient(BaseClient):
    """Клиент для работы с Account API."""

    @allure.step("Регистрируем пользователя: {payload}")
    def register(self, payload: dict) -> RegisterResponseSchema:
        """Регистрирует нового пользователя."""
        validate_register_request(payload)
        logger.info(f"Регистрируем пользователя: {payload}")
        response = self.send_request(
            HTTPMethod.POST,
            REGISTER_URL,
            json=payload,
        )
        self.check_status_code(response, 201)
        return validate_register_response(response.json())

    @allure.step("Регистрируем пользователя с ошибкой, ожидаем {expected_code}")
    def register_expect_error(
        self,
        payload: dict,
        expected_code: int,
    ) -> ErrorResponseSchema:
        """Проверяет регистрацию с ожидаемой ошибкой."""
        response = self.send_request(
            HTTPMethod.POST,
            REGISTER_URL,
            json=payload,
        )
        self.check_status_code(response, expected_code)
        return validate_error_response(response.json())

    @allure.step("Получаем токен для пользователя: {payload}")
    def generate_token(self, payload: dict) -> TokenResponseSchema:
        """Возвращает токен авторизации пользователя."""
        validate_login_request(payload)
        logger.info(f"Авторизуем пользователя: {payload}")
        response = self.send_request(
            HTTPMethod.POST,
            LOGIN_URL,
            json=payload,
        )
        self.check_status_code(response, 200)
        return validate_token_response(response.json())

    @allure.step("Получаем токен с ошибкой, ожидаем {expected_code}")
    def generate_token_expect_error(
        self,
        payload: dict,
        expected_code: int,
    ) -> ErrorResponseSchema:
        """Проверяет авторизацию с ожидаемой ошибкой."""
        response = self.send_request(
            HTTPMethod.POST,
            LOGIN_URL,
            json=payload,
        )
        self.check_status_code(response, expected_code)
        return validate_error_response(response.json())

    @allure.step("Проверяем авторизацию пользователя: {payload}")
    def authorize(self, payload: dict) -> bool:
        """Проверяет авторизацию пользователя."""
        validate_login_request(payload)
        response = self.send_request(
            HTTPMethod.POST,
            CHECKUSER_URL,
            json=payload,
        )
        self.check_status_code(response, 200)
        return bool(response.json())

    @allure.step("Проверяем авторизацию с ошибкой, ожидаем {expected_code}")
    def authorize_expect_error(
        self,
        payload: dict,
        expected_code: int,
    ) -> ErrorResponseSchema:
        """Проверяет авторизацию с ожидаемой ошибкой."""
        response = self.send_request(
            HTTPMethod.POST,
            CHECKUSER_URL,
            json=payload,
        )
        self.check_status_code(response, expected_code)
        return validate_error_response(response.json())

    @allure.step("Получаем профиль пользователя с ID: {user_id}")
    def get_profile(
        self,
        user_id: str,
        token: str,
    ) -> ProfileResponseSchema:
        """Возвращает профиль пользователя с книгами."""
        logger.info(f"Получаем профиль пользователя с ID: {user_id}")
        response = self.send_request(
            HTTPMethod.GET,
            f"{USER_URL}{user_id}",
            headers=self.auth_headers(token),
        )
        self.check_status_code(response, 200)
        return validate_profile_response(response.json())

    @allure.step("Получаем профиль с ошибкой, ожидаем {expected_code}")
    def get_profile_expect_error(
        self,
        user_id: str,
        token: str,
        expected_code: int,
    ) -> ErrorResponseSchema:
        """Проверяет получение профиля с ожидаемой ошибкой."""
        response = self.send_request(
            HTTPMethod.GET,
            f"{USER_URL}{user_id}",
            headers=self.auth_headers(token),
        )
        self.check_status_code(response, expected_code)
        return validate_error_response(response.json())
