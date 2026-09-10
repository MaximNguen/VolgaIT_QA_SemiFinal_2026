import logging
import allure

from selenium.webdriver.support.ui import WebDriverWait

from UI_Service.pages.base_page import BasePage
from data.ui_data.locators_ads import AdsPageLocators as ADL
from config import AD_DISPLAY_TIMEOUT_SECONDS

logger = logging.getLogger(__name__)


class AdsPage(BasePage):
    """Класс для взаимодействия со страницей «Рекламные окна»."""

    def __init__(self, driver):
        super().__init__(driver)

    def get_countdown_text(self) -> str:
        """Получить текст обратного отсчёта."""
        with allure.step("Получаем текст обратного отсчёта"):
            logger.info("Получаем текст обратного отсчёта")
            return self.get_text(*ADL.countdown_text)

    def wait_for_ad(self) -> None:
        """Дождаться появления рекламного окна."""
        with allure.step("Ожидаем появления рекламного окна"):
            logger.info("Ожидаем появления рекламного окна")
            self.wait.wait_until_class_contains(
                ADL.popup, "pum-active", timeout=AD_DISPLAY_TIMEOUT_SECONDS
            )

    def is_ad_active(self) -> bool:
        """Проверить, отображается ли рекламное окно."""
        with allure.step("Проверяем, отображается ли рекламное окно"):
            logger.info("Проверяем, отображается ли рекламное окно")
            element = self.driver.find_element(*ADL.popup)
            return "pum-active" in element.get_attribute("class")

    def get_ad_title(self) -> str:
        """Получить заголовок рекламного окна."""
        with allure.step("Получаем заголовок рекламного окна"):
            logger.info("Получаем заголовок рекламного окна")
            return self.get_text(*ADL.popup_title)

    def get_ad_text(self) -> str:
        """Получить текст рекламного окна."""
        with allure.step("Получаем текст рекламного окна"):
            logger.info("Получаем текст рекламного окна")
            return self.get_text(*ADL.popup_content)

    def click_close_ad(self) -> None:
        """Закрыть рекламное окно кнопкой «×»."""
        with allure.step("Закрываем рекламное окно кнопкой «×»"):
            logger.info("Закрываем рекламное окно кнопкой «×»")
            self.click(*ADL.popup_close)
            WebDriverWait(self.driver, 5).until_not(
                lambda d: "pum-active" in d.find_element(*ADL.popup).get_attribute("class")
            )

    def is_main_content_displayed(self) -> bool:
        """Проверить, отображается ли основной контент страницы."""
        with allure.step("Проверяем, отображается ли основной контент страницы"):
            logger.info("Проверяем, отображается ли основной контент страницы")
            return self.is_element_displayed(*ADL.main_content)

    def click_overlay(self) -> None:
        """Клик по подложке рекламного окна."""
        with allure.step("Кликаем по подложке рекламного окна"):
            logger.info("Кликаем по подложке рекламного окна")
            element = self.find_element(*ADL.popup)
            self.driver.execute_script("arguments[0].click();", element)
