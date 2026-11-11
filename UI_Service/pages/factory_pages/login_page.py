import logging
import allure

from selenium.webdriver.support.ui import WebDriverWait

from UI_Service.pages.base_page import BasePage
from data.ui_data.locators_login import LoginPageLocators as LPL

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Класс для взаимодействия со страницей авторизации."""

    def __init__(self, driver):
        super().__init__(driver)

    def check_login_header_loaded(self) -> bool:
        """Проверить, что заголовок страницы авторизации загружен."""
        with allure.step("Проверяем, что заголовок авторизации загружен"):
            logger.info("Проверяем, что заголовок авторизации загружен")
            return self.find_element(*LPL.login_header).is_displayed()

    def input_username(self, username: str) -> None:
        """Ввести имя пользователя."""
        with allure.step(f"Вводим имя пользователя: {username}"):
            logger.info(f"Вводим имя пользователя: {username}")
            username_input = self.find_element(*LPL.username_input)
            self.input_text(username_input, username)

    def input_password(self, password: str) -> None:
        """Ввести пароль пользователя."""
        with allure.step(f"Вводим пароль пользователя: {password}"):
            logger.info(f"Вводим пароль пользователя: {password}")
            password_input = self.find_element(*LPL.password_input)
            self.input_text(password_input, password)

    def click_login_button(self) -> None:
        """Кликнуть на кнопку входа."""
        with allure.step("Кликаем на кнопку входа"):
            logger.info("Кликаем на кнопку входа")
            self.click(*LPL.login_button)