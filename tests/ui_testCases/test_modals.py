import logging

import allure
import pytest

from data.ui_data.urls import modals_url
from data.ui_data.locators_modals import ModalsPageLocators as MPL
from data.ui_data.mock_data import test_name, valid_email, invalid_email, whitespace_name
from data.ui_data.expected_data import (
    expected_simple_modal_title,
    expected_simple_modal_text,
    expected_success_message,
    expected_required_field_message,
    expected_invalid_email_message,
    expected_form_errors_message,
)

logger = logging.getLogger(__name__)


@allure.epic("Страница «Модальные окна»")
@allure.feature("Проверка функционала модальных окон")
class TestModalsPage:
    """Тест-кейсы для страницы модальных окон."""

    @pytest.fixture(autouse=True)
    def setup(self, modals_page):
        self.modals_page = modals_page
        self.modals_page.open(modals_url)
        yield

    @allure.title("Простое модальное окно открывается по клику")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_simple_modal_opens(self):
        logger.info("Проверяем открытие простого модального окна")
        self.modals_page.click_simple_modal()
        self.modals_page.wait_for_simple_modal()
        assert self.modals_page.is_simple_modal_active()

    @allure.title("Содержимое простого модального окна")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_simple_modal_content(self):
        logger.info("Проверяем содержимое простого модального окна")
        self.modals_page.click_simple_modal()
        self.modals_page.wait_for_simple_modal()
        assert self.modals_page.get_simple_modal_title() == expected_simple_modal_title
        assert self.modals_page.get_simple_modal_text() == expected_simple_modal_text

    @allure.title("Простое модальное окно закрывается кнопкой «×»")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_simple_modal_closes(self):
        logger.info("Проверяем закрытие простого модального окна")
        self.modals_page.click_simple_modal()
        self.modals_page.wait_for_simple_modal()
        self.modals_page.close_simple_modal()
        assert not self.modals_page.is_simple_modal_active()

    @allure.title("Модальное окно с формой открывается по клику")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_form_modal_opens(self):
        logger.info("Проверяем открытие модального окна с формой")
        self.modals_page.click_form_modal()
        self.modals_page.wait_for_form_modal()
        assert self.modals_page.is_form_modal_active()

    @allure.title("Модальное окно с формой содержит поля Name, Email, Message и Submit")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_form_modal_has_fields(self):
        logger.info("Проверяем наличие полей в модальном окне с формой")
        self.modals_page.click_form_modal()
        self.modals_page.wait_for_form_modal()
        assert self.modals_page.is_element_displayed(*MPL.form_popup_name)
        assert self.modals_page.is_element_displayed(*MPL.form_popup_email)
        assert self.modals_page.is_element_displayed(*MPL.form_popup_message)
        assert self.modals_page.is_element_displayed(*MPL.form_popup_submit)

    @allure.title("Валидная отправка формы показывает сообщение об успехе")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_form_modal_valid_submit(self):
        logger.info("Проверяем успешную отправку формы")
        self.modals_page.click_form_modal()
        self.modals_page.wait_for_form_modal()
        self.modals_page.enter_name(test_name)
        self.modals_page.enter_email(valid_email)
        self.modals_page.enter_message("Hello")
        self.modals_page.click_submit()
        assert self.modals_page.is_success_displayed()
        assert self.modals_page.get_success_message() == expected_success_message

    @allure.title("Кнопка «← Back» возвращает к форме")
    @allure.severity(allure.severity_level.NORMAL)
    def test_form_modal_back_button(self):
        logger.info("Проверяем возврат к форме через кнопку «← Back»")
        self.modals_page.click_form_modal()
        self.modals_page.wait_for_form_modal()
        self.modals_page.enter_name(test_name)
        self.modals_page.click_submit()
        assert self.modals_page.is_success_displayed()
        self.modals_page.click_back()
        assert self.modals_page.is_element_displayed(*MPL.form_popup_name)

    @allure.title("Модальное окно с формой закрывается кнопкой «×»")
    @allure.severity(allure.severity_level.NORMAL)
    def test_form_modal_closes(self):
        logger.info("Проверяем закрытие модального окна с формой")
        self.modals_page.click_form_modal()
        self.modals_page.wait_for_form_modal()
        self.modals_page.close_form_modal()
        assert not self.modals_page.is_form_modal_active()

    @allure.title("Отправка пустой формы показывает ошибку обязательного поля")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_form_modal_empty_submit(self):
        logger.info("Проверяем отправку пустой формы")
        self.modals_page.click_form_modal()
        self.modals_page.wait_for_form_modal()
        self.modals_page.click_submit()
        assert self.modals_page.get_name_error() == expected_required_field_message

    @allure.title("Имя из пробелов отклоняется")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_form_modal_whitespace_name(self):
        logger.info("Проверяем отклонение имени из пробелов")
        self.modals_page.click_form_modal()
        self.modals_page.wait_for_form_modal()
        self.modals_page.enter_name(whitespace_name)
        self.modals_page.click_submit()
        assert self.modals_page.get_name_error() == expected_required_field_message

    @allure.title("Невалидный email отклоняется")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_form_modal_invalid_email(self):
        logger.info("Проверяем отклонение невалидного email")
        self.modals_page.click_form_modal()
        self.modals_page.wait_for_form_modal()
        self.modals_page.enter_name(test_name)
        self.modals_page.enter_email(invalid_email)
        self.modals_page.click_submit()
        assert self.modals_page.get_email_error() == expected_invalid_email_message

    @allure.title("Блок ошибок формы отображается при невалидной отправке")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_form_modal_errors_block(self):
        logger.info("Проверяем отображение блока ошибок формы")
        self.modals_page.click_form_modal()
        self.modals_page.wait_for_form_modal()
        self.modals_page.click_submit()
        assert self.modals_page.is_form_errors_block_displayed()
        assert expected_form_errors_message in self.modals_page.get_form_errors_message()
