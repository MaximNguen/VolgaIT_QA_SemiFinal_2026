import logging

import allure

from utils.api.payloads import build_user_payload, get_invalid_password

logger = logging.getLogger(__name__)


@allure.epic("API - Account")
@allure.feature("Регистрация пользователя")
class TestRegisterUserEndpoint:
    """Тесты регистрации пользователя."""

    @allure.title("Успешная регистрация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_success(self, user_client):
        """API создаёт пользователя и возвращает его данные."""
        payload = build_user_payload()
        user = user_client.register(payload)

        assert user.userID, "Не получен userID"
        assert user.username == payload["userName"]
        assert user.books == []

    @allure.title("Повторная регистрация существующего пользователя")
    def test_register_duplicate_user(self, user_client, api_user):
        """Повторная регистрация возвращает ошибку 406."""
        error = user_client.register_expect_error(
            api_user["payload"],
            expected_code=406,
        )

        assert error.code == "1204"
        assert "exists" in error.message.lower()

    @allure.title("Регистрация с паролем, не проходящим валидацию")
    def test_register_invalid_password(self, user_client):
        """Слишком короткий пароль отклоняется API."""
        payload = build_user_payload(
            password=get_invalid_password(),
            validate=False,
        )
        error = user_client.register_expect_error(payload, expected_code=400)

        assert error.code == "1300"
        assert "Passwords must" in error.message
