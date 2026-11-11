import logging
import allure

from selenium.webdriver.support.ui import WebDriverWait

from UI_Service.pages.base_page import BasePage
from data.ui_data.locators_registration import RegisterPageLocators as RPL

logger = logging.getLogger(__name__)


class RegisterPage(BasePage):
    """Класс для взаимодействия со страницей регистрации."""
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def check_registration_header_loaded(self) -> bool:
        """Проверить, что заголовок страницы регистрации загружен."""
        with allure.step("Проверяем, что заголовок регистрации загружен"):
            logger.info("Проверяем, что заголовок регистрации загружен")
            return self.find_element(*RPL.register_header).is_displayed()
        
    def input_first_name(self, first_name: str) -> None:
        """Ввести имя пользователя."""
        with allure.step(f"Вводим имя пользователя: {first_name}"):
            logger.info(f"Вводим имя пользователя: {first_name}")
            first_name_input = self.find_element(*RPL.first_name_input)
            self.input_text(first_name_input, first_name)
    
    def input_last_name(self, last_name: str) -> None:
        """Ввести фамилию пользователя."""
        with allure.step(f"Вводим фамилию пользователя: {last_name}"):
            logger.info(f"Вводим фамилию пользователя: {last_name}")
            last_name_input = self.find_element(*RPL.last_name_input)
            self.input_text(last_name_input, last_name)
            
    def input_user_name(self, user_name: str) -> None:
        """Ввести имя пользователя для регистрации."""
        with allure.step(f"Вводим имя пользователя: {user_name}"):
            logger.info(f"Вводим имя пользователя: {user_name}")
            user_name_input = self.find_element(*RPL.user_name_input)
            self.input_text(user_name_input, user_name)
    
    def input_password(self, password: str) -> None:
        """Ввести пароль пользователя для регистрации."""
        with allure.step(f"Вводим пароль пользователя: {password}"):
            logger.info(f"Вводим пароль пользователя: {password}")
            password_input = self.find_element(*RPL.password_input)
            self.input_text(password_input, password)
    
    def click_submit_button(self) -> None:
        """Кликнуть на кнопку регистрации."""
        with allure.step("Кликаем на кнопку регистрации"):
            logger.info("Кликаем на кнопку регистрации")
            self.click(*RPL.submit_button)