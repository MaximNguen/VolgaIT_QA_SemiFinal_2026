import logging

import allure
import pytest

from data.ui_data.urls import ads_url
from data.ui_data.expected_data import (
    expected_countdown_text,
    expected_ad_title,
    expected_ad_text,
)

logger = logging.getLogger(__name__)


@allure.epic("Страница «Рекламные окна»")
@allure.feature("Проверка функционала рекламных окон")
class TestAdsPage:
    """Тест-кейсы для страницы рекламных окон."""

    @pytest.fixture(autouse=True)
    def setup(self, ads_page):
        self.ads_page = ads_page
        self.ads_page.open(ads_url)
        yield

    @allure.title("Текст обратного отсчёта отображается")
    @allure.severity(allure.severity_level.NORMAL)
    def test_countdown_text(self):
        logger.info("Проверяем текст обратного отсчёта")
        assert self.ads_page.get_countdown_text() == expected_countdown_text

    @allure.title("Реклама появляется через несколько секунд")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ad_appears_after_timeout(self):
        logger.info("Ожидаем появления рекламного окна")
        self.ads_page.wait_for_ad()
        assert self.ads_page.is_ad_active()

    @allure.title("Содержимое рекламного окна")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ad_content(self):
        logger.info("Проверяем содержимое рекламного окна")
        self.ads_page.wait_for_ad()
        assert self.ads_page.get_ad_title() == expected_ad_title
        assert self.ads_page.get_ad_text() == expected_ad_text

    @allure.title("Реклама закрывается кнопкой «×»")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ad_closes(self):
        logger.info("Проверяем закрытие рекламного окна")
        self.ads_page.wait_for_ad()
        self.ads_page.click_close_ad()
        assert not self.ads_page.is_ad_active()

    @allure.title("Основной контент доступен после закрытия рекламы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_main_content_accessible_after_close(self):
        logger.info("Проверяем доступность контента после закрытия рекламы")
        self.ads_page.wait_for_ad()
        self.ads_page.click_close_ad()
        assert self.ads_page.is_main_content_displayed()

    @allure.title("Реклама перекрывает контент страницы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ad_overlays_content(self):
        logger.info("Проверяем, что реклама отображается поверх контента")
        self.ads_page.wait_for_ad()
        assert self.ads_page.is_ad_active()
        assert self.ads_page.is_main_content_displayed()

    @allure.title("Реклама появляется снова после перезагрузки страницы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ad_appears_again_after_reload(self):
        logger.info("Проверяем повторное появление рекламы после перезагрузки")
        self.ads_page.wait_for_ad()
        self.ads_page.click_close_ad()
        self.ads_page.open(ads_url)
        self.ads_page.wait_for_ad()
        assert self.ads_page.is_ad_active()

    @allure.title("Сразу после загрузки реклама не отображается")
    @allure.severity(allure.severity_level.NORMAL)
    def test_ad_not_visible_immediately(self):
        logger.info("Проверяем, что реклама не видна сразу после загрузки")
        assert not self.ads_page.is_ad_active()

    @allure.title("Клавиша Escape не закрывает рекламу")
    @allure.severity(allure.severity_level.NORMAL)
    def test_escape_does_not_close_ad(self):
        logger.info("Проверяем, что Escape не закрывает рекламу")
        self.ads_page.wait_for_ad()
        self.ads_page.press_escape()
        assert self.ads_page.is_ad_active()

    @allure.title("Клик по подложке не закрывает рекламу")
    @allure.severity(allure.severity_level.NORMAL)
    def test_overlay_click_does_not_close_ad(self):
        logger.info("Проверяем, что клик по подложке не закрывает рекламу")
        self.ads_page.wait_for_ad()
        self.ads_page.click_overlay()
        assert self.ads_page.is_ad_active()
