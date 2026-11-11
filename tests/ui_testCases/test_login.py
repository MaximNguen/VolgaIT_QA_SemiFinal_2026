import logging

import allure

from data.ui_data.expected_data import invalid_login
from data.ui_data.mock_data import (
    invalid_login_password,
    unknown_login,
    valid_login,
)
from data.ui_data.urls import login_page_url


logger = logging.getLogger(__name__)


@allure.epic("Страница авторизации")
@allure.feature("Проверка функционала авторизации")
class TestLoginPage:
    """Тест-кейсы для страницы авторизации."""

    @allure.title("Страница авторизации загружается")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_page_loaded(self, login_page):
        """Заголовок страницы авторизации отображается."""
        login_page.open(login_page_url)
        assert login_page.check_login_header_loaded(), (
            "Заголовок страницы авторизации не отображается"
        )

    @allure.title("Успешная авторизация зарегистрированного пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login(self, login_page, profile_page):
        """Вход под тестовым пользователем переводит в профиль с его именем."""
        username, password = valid_login
        login_page.open(login_page_url)
        login_page.login(username, password)
        login_page.wait_until_logged_in()
        assert profile_page.get_username() == username

    @allure.title("Авторизация с неверным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_password(self, login_page, profile_page):
        """Неверный пароль не авторизует пользователя."""
        username, password = valid_login
        login_page.open(login_page_url)
        login_page.login(username, password)
        login_page.wait_until_logged_in()
        profile_page.logout()
        login_page.login(username, invalid_login_password)
        assert login_page.get_error_text() == invalid_login
        assert "/login" in login_page.get_current_url()

    @allure.title("Авторизация незарегистрированного пользователя")
    def test_unknown_user(self, login_page):
        """Несуществующий пользователь не авторизуется."""
        login_page.open(login_page_url)
        login_page.login(*unknown_login)
        assert login_page.get_error_text() == invalid_login

    @allure.title("Пустые логин и пароль не выполняют вход")
    def test_empty_credentials(self, login_page):
        """Пустые логин и пароль не авторизуют пользователя."""
        login_page.open(login_page_url)
        login_page.click_login_button()
        assert "/login" in login_page.get_current_url()
        assert login_page.check_login_header_loaded()

    @allure.title("Кнопка New User открывает страницу регистрации")
    def test_new_user_button_opens_registration(self, login_page, register_page):
        """Кнопка New User переводит на страницу регистрации."""
        login_page.open(login_page_url)
        login_page.click_new_user_button()
        if not login_page.wait.wait_for_url_contains("/register", timeout=5):
            login_page.click_new_user_button()
        assert login_page.wait.wait_for_url_contains("/register")
        assert register_page.check_registration_header_loaded(), (
            "Страница регистрации не открылась"
        )

    @allure.title("Выход из аккаунта возвращает на страницу авторизации")
    def test_logout(self, login_page, profile_page):
        """После выхода из аккаунта отображается форма авторизации."""
        username, password = valid_login
        login_page.open(login_page_url)
        login_page.login(username, password)
        login_page.wait_until_logged_in()
        profile_page.logout()
        assert login_page.check_login_header_loaded(), (
            "После выхода не отображается страница авторизации"
        )
