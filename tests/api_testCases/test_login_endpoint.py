import logging

import allure

from utils.api.payloads import build_user_payload, get_wrong_password

logger = logging.getLogger(__name__)


@allure.epic("API - Account")
@allure.feature("Авторизация пользователя")
class TestLoginUserEndpoint:
    """Тесты авторизации пользователя."""

    @allure.title("Успешное получение токена авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_generate_token_success(self, user_client, api_user):
        """Валидные учётные данные возвращают токен."""
        token = user_client.generate_token(api_user["payload"])

        assert token.status == "Success"
        assert token.token, "Токен не получен"
        assert token.result == "User authorized successfully."

    @allure.title("Получение токена с неверным паролем")
    def test_generate_token_wrong_password(self, user_client, api_user):
        """Неверный пароль возвращает статус Failed без токена."""
        payload = build_user_payload(
            username=api_user["username"],
            password=get_wrong_password(),
        )
        token = user_client.generate_token(payload)

        assert token.status == "Failed"
        assert token.token is None
        assert token.result == "User authorization failed."

    @allure.title("Получение токена с пустыми данными")
    def test_generate_token_empty_payload(self, user_client):
        """Пустой запрос отклоняется с кодом 1200."""
        error = user_client.generate_token_expect_error(
            {},
            expected_code=400,
        )

        assert error.code == "1200"
        assert error.message == "UserName and Password required."

    @allure.title("Проверка авторизации валидного пользователя")
    def test_authorize_success(self, user_client, api_user):
        """Authorized возвращает True для валидных данных."""
        assert user_client.authorize(api_user["payload"]) is True

    @allure.title("Проверка авторизации с неверным паролем")
    def test_authorize_wrong_password(self, user_client, api_user):
        """Authorized возвращает 404 для неверного пароля."""
        payload = build_user_payload(
            username=api_user["username"],
            password=get_wrong_password(),
        )
        error = user_client.authorize_expect_error(
            payload,
            expected_code=404,
        )

        assert error.code == "1207"
        assert error.message == "User not found!"
