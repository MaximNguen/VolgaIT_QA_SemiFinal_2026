import logging
from typing import List

import allure

from UI_Service.pages.base_page import BasePage
from data.ui_data.locators_form_fields import FormFieldsPageLocators as FFL

logger = logging.getLogger(__name__)


class FormFieldsPage(BasePage):
    """Класс для взаимодействия со страницей «Форма»."""

    def __init__(self, driver):
        super().__init__(driver)

    def enter_name(self, text: str) -> None:
        """Ввести имя в поле Name."""
        with allure.step(f"Вводим имя '{text}' в поле Name"):
            logger.info(f"Вводим имя '{text}' в поле Name")
            self.input_text(self.find_element(*FFL.name_input), text)

    def get_automation_tools(self) -> List[str]:
        """Получить список элементов раздела «Automation tools»."""
        with allure.step("Получаем список элементов раздела «Automation tools»"):
            logger.info("Получаем список элементов раздела «Automation tools»")
            elements = self.find_elements(*FFL.automation_tools_items)
            return [element.text.strip() for element in elements if element.text.strip()]

    def get_automation_tools_message(self) -> str:
        """Получить текст списка «Automation tools» через запятую."""
        with allure.step("Получаем текст списка «Automation tools» через запятую"):
            logger.info("Получаем текст списка «Automation tools» через запятую")
            return ", ".join(self.get_automation_tools())

    def fill_message_with_automation_tools(self) -> None:
        """Заполнить поле Message списком «Automation tools»."""
        with allure.step("Заполняем поле Message списком «Automation tools»"):
            logger.info("Заполняем поле Message списком «Automation tools»")
            self.input_text(
                self.find_element(*FFL.message_input),
                self.get_automation_tools_message(),
            )

    def get_message_value(self) -> str:
        """Получить значение поля Message."""
        with allure.step("Получаем значение поля Message"):
            logger.info("Получаем значение поля Message")
            return self.get_attribute_data(*FFL.message_input, attribute="value")

    def click_submit(self) -> None:
        """Клик по кнопке Submit."""
        with allure.step("Кликаем по кнопке Submit"):
            logger.info("Кликаем по кнопке Submit")
            submit = self.find_element(*FFL.submit_button)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", submit
            )
            self.driver.execute_script("arguments[0].click();", submit)
