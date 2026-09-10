import logging
import allure

from UI_Service.pages.base_page import BasePage
from data.ui_data.locators_calendars import CalendarPageLocators as CL

logger = logging.getLogger(__name__)


class CalendarPage(BasePage):
    """Класс для взаимодействия со страницей «Календарь»."""

    def __init__(self, driver):
        super().__init__(driver)

    def get_heading(self) -> str:
        """Получить заголовок страницы."""
        with allure.step("Получаем заголовок страницы"):
            logger.info("Получаем заголовок страницы")
            return self.get_text(*CL.heading)

    def is_date_input_displayed(self) -> bool:
        """Проверить, отображается ли поле даты."""
        with allure.step("Проверяем, отображается ли поле даты"):
            logger.info("Проверяем, отображается ли поле даты")
            return self.is_element_displayed(*CL.date_input)

    def enter_date(self, date_value: str) -> None:
        """Ввести дату в поле."""
        with allure.step(f"Вводим дату '{date_value}' в поле даты"):
            logger.info(f"Вводим дату '{date_value}' в поле даты")
            self.input_text(self.find_element(*CL.date_input), date_value)

    def get_date_input_value(self) -> str:
        """Получить значение поля даты."""
        with allure.step("Получаем значение поля даты"):
            logger.info("Получаем значение поля даты")
            return self.get_attribute_data(*CL.date_input, attribute="value")

    def click_submit(self) -> None:
        """Клик по кнопке Submit."""
        with allure.step("Кликаем по кнопке Submit"):
            logger.info("Кликаем по кнопке Submit")
            self.click(*CL.submit_button)

    def is_success_block_displayed(self) -> bool:
        """Проверить, отображается ли блок успешной отправки."""
        with allure.step("Проверяем, отображается ли блок успешной отправки"):
            logger.info("Проверяем, отображается ли блок успешной отправки")
            return self.is_element_displayed(*CL.success_block)

    def get_success_message(self) -> str:
        """Получить текст сообщения об успехе."""
        with allure.step("Получаем текст сообщения об успехе"):
            logger.info("Получаем текст сообщения об успехе")
            return self.get_text(*CL.success_heading)

    def get_submitted_date_summary(self) -> str:
        """Получить текст сводки с отправленной датой."""
        with allure.step("Получаем текст сводки с отправленной датой"):
            logger.info("Получаем текст сводки с отправленной датой")
            return self.get_text(*CL.success_summary)

    def click_back(self) -> None:
        """Клик по кнопке «← Back»."""
        with allure.step("Кликаем по кнопке «← Back»"):
            logger.info("Кликаем по кнопке «← Back»")
            self.click(*CL.back_button)

    def get_date_error_message(self) -> str:
        """Получить текст ошибки валидации даты."""
        with allure.step("Получаем текст ошибки валидации даты"):
            logger.info("Получаем текст ошибки валидации даты")
            return self.get_text(*CL.date_error_message)

    def is_form_errors_block_displayed(self) -> bool:
        """Проверить, отображается ли блок ошибок формы."""
        with allure.step("Проверяем, отображается ли блок ошибок формы"):
            logger.info("Проверяем, отображается ли блок ошибок формы")
            return self.is_element_displayed(*CL.form_errors_block)
