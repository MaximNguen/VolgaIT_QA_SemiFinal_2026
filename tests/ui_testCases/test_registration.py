import logging

import allure
import pytest

from data.ui_data.urls import registration_page_url
from data.ui_data.mock_data import valid_registration, invalid_registration
from data.ui_data.expected_data import success

logger = logging.getLogger(__name__)


@pytest.mark.skip(reason="Регистрация на demoqa нестабильна (форма сбрасывается при инициализации reCAPTCHA)")
@allure.epic("Страница регистрации")
@allure.feature("Проверка функционала регистрации")
class TestRegistrationPage:
    """Тест-кейсы для страницы регистрации."""

    @pytest.fixture(autouse=True)
    def setup(self, register_page):
        self.register_page = register_page
        self.register_page.open(registration_page_url)
        yield

    @allure.title("Успешная регистрация с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "first_name, last_name, user, password",
        valid_registration,
    )
    def test_valid_registration(self, first_name, last_name, user, password):
        """Валидная регистрация"""
        logger.info(
            f"Вводим данные для регистрации - {first_name}, {last_name}, {user}, {password}"
        )
        self.register_page.input_first_name(first_name)
        self.register_page.input_last_name(last_name)
        self.register_page.input_user_name(user)
        self.register_page.input_password(password)
        self.register_page.click_submit_button()
        text = self.register_page.accept_alert()
        assert text == success, (
            f"Регистрация не прошла, данные - {first_name} {last_name} {user} {password}"
        )

    @allure.title("Невалидная регистрация с невалидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "first_name, last_name, user, password",
        invalid_registration,
    )
    def test_invalid_registration(self, first_name, last_name, user, password):
        """Регистрация с невалидным паролем не выполняется"""
        logger.info(
            f"Вводим данные для регистрации - {first_name}, {last_name}, {user}, {password}"
        )
        self.register_page.input_first_name(first_name)
        self.register_page.input_last_name(last_name)
        self.register_page.input_user_name(user)
        self.register_page.input_password(password)
        self.register_page.click_submit_button()
        assert self.register_page.get_current_url() == registration_page_url, (
            f"Регистрация прошла с невалидным паролем, данные - "
            f"{first_name} {last_name} {user} {password}"
        )
