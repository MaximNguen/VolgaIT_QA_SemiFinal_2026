import logging
from datetime import date

import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait

from data.ui_data.urls import calendars_url
from data.ui_data.mock_data import (
    valid_date,
    leap_year_date,
    future_date,
    past_date,
    invalid_dates,
)
from data.ui_data.expected_data import (
    expected_calendars_heading,
    expected_success_message,
    expected_invalid_date_message,
)

logger = logging.getLogger(__name__)


@allure.epic("Страница «Календарь»")
@allure.feature("Проверка функционала календаря")
class TestCalendarPage:
    """Тест-кейсы для страницы календаря."""

    @pytest.fixture(autouse=True)
    def setup(self, calendar_page):
        self.calendar_page = calendar_page
        self.calendar_page.open(calendars_url)
        yield

    @allure.title("Открытие страницы календаря")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_page_heading(self):
        logger.info("Проверяем заголовок страницы календаря")
        assert self.calendar_page.get_heading() == expected_calendars_heading
        assert self.calendar_page.is_date_input_displayed()

    @allure.title("Поле даты принимает валидную дату")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_date_input_accepts_valid_date(self):
        logger.info("Проверяем, что поле даты принимает валидную дату")
        self.calendar_page.enter_date(valid_date)
        assert self.calendar_page.get_date_input_value() == valid_date

    @allure.title("Отправка валидной даты показывает сообщение об успехе")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submit_valid_date_success(self):
        logger.info("Проверяем успешную отправку валидной даты")
        self.calendar_page.enter_date(valid_date)
        self.calendar_page.click_submit()
        assert self.calendar_page.is_success_block_displayed()
        assert self.calendar_page.get_success_message() == expected_success_message

    @allure.title("В ответе отображается выбранная дата")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submitted_date_displayed(self):
        logger.info("Проверяем, что выбранная дата отображается в ответе")
        self.calendar_page.enter_date(valid_date)
        self.calendar_page.click_submit()
        assert valid_date in self.calendar_page.get_submitted_date_summary()

    @allure.title("Високосная дата принимается")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_leap_year_date(self):
        logger.info("Проверяем приём високосной даты")
        self.calendar_page.enter_date(leap_year_date)
        self.calendar_page.click_submit()
        assert self.calendar_page.is_success_block_displayed()

    @allure.title("Сегодняшняя дата принимается")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_today_date(self):
        logger.info("Проверяем приём сегодняшней даты")
        today = date.today().strftime("%Y-%m-%d")
        self.calendar_page.enter_date(today)
        self.calendar_page.click_submit()
        assert self.calendar_page.is_success_block_displayed()

    @allure.title("Будущая дата принимается")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_future_date(self):
        logger.info("Проверяем приём будущей даты")
        self.calendar_page.enter_date(future_date)
        self.calendar_page.click_submit()
        assert self.calendar_page.is_success_block_displayed()

    @allure.title("Прошлая дата принимается")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_past_date(self):
        logger.info("Проверяем приём прошлой даты")
        self.calendar_page.enter_date(past_date)
        self.calendar_page.click_submit()
        assert self.calendar_page.is_success_block_displayed()

    @allure.title("URL после успешной отправки содержит contact-form-sent")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_redirects_with_sent_param(self):
        logger.info("Проверяем URL после успешной отправки")
        self.calendar_page.enter_date(valid_date)
        self.calendar_page.click_submit()
        WebDriverWait(self.calendar_page.driver, 15).until(
            lambda d: "contact-form-sent" in d.current_url
        )
        assert "contact-form-sent" in self.calendar_page.get_current_url()

    @allure.title("Кнопка «← Back» возвращает к форме")
    @allure.severity(allure.severity_level.NORMAL)
    def test_back_button_returns_to_form(self):
        logger.info("Проверяем возврат к форме через кнопку «← Back»")
        self.calendar_page.enter_date(valid_date)
        self.calendar_page.click_submit()
        self.calendar_page.click_back()
        assert self.calendar_page.is_date_input_displayed()

    @allure.title("Текстовое значение отклоняется")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_text_date(self):
        logger.info("Проверяем отклонение текстового значения")
        self.calendar_page.enter_date(invalid_dates[0])
        self.calendar_page.click_submit()
        assert self.calendar_page.get_date_error_message() == expected_invalid_date_message

    @allure.title("Неполная дата отклоняется")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_incomplete_date(self):
        logger.info("Проверяем отклонение неполной даты")
        self.calendar_page.enter_date(invalid_dates[1])
        self.calendar_page.click_submit()
        assert self.calendar_page.get_date_error_message() == expected_invalid_date_message

    @allure.title("Несуществующая дата отклоняется")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_nonexistent_date(self):
        logger.info("Проверяем отклонение несуществующей даты")
        self.calendar_page.enter_date(invalid_dates[2])
        self.calendar_page.click_submit()
        assert self.calendar_page.get_date_error_message() == expected_invalid_date_message

    @allure.title("Дата в чужом формате отклоняется")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_wrong_format_date(self):
        logger.info("Проверяем отклонение даты в другом формате")
        self.calendar_page.enter_date(invalid_dates[3])
        self.calendar_page.click_submit()
        assert self.calendar_page.get_date_error_message() == expected_invalid_date_message
