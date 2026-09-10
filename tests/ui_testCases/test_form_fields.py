import logging

import allure
import pytest

from data.ui_data.urls import form_fields_url
from data.ui_data.mock_data import test_name
from data.ui_data.expected_data import (
    expected_automation_tools,
    expected_automation_tools_message,
    expected_alert_message,
)

logger = logging.getLogger(__name__)


@allure.epic("Страница «Форма»")
@allure.feature("Задание №5 — заполнение Message списком Automation tools")
class TestFormFieldsPage:
    """Тест-кейсы для страницы формы."""

    @pytest.fixture(autouse=True)
    def setup(self, form_fields_page):
        self.form_fields_page = form_fields_page
        self.form_fields_page.open(form_fields_url)
        yield

    @allure.title("Раздел «Automation tools» содержит ожидаемый список")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_automation_tools_list(self):
        logger.info("Проверяем список элементов раздела «Automation tools»")
        tools = self.form_fields_page.get_automation_tools()
        assert tools == expected_automation_tools

    @allure.title("Поле Message заполнено списком Automation tools через запятую")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_message_filled_with_automation_tools(self):
        logger.info("Проверяем заполнение поля Message списком Automation tools")
        self.form_fields_page.fill_message_with_automation_tools()
        assert self.form_fields_page.get_message_value() == expected_automation_tools_message

    @allure.title("Отправка формы с заполненным Message показывает alert")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_shows_alert(self):
        logger.info("Проверяем появление alert при отправке формы")
        self.form_fields_page.enter_name(test_name)
        self.form_fields_page.fill_message_with_automation_tools()
        self.form_fields_page.click_submit()
        alert_text = self.form_fields_page.accept_alert()
        assert alert_text == expected_alert_message
