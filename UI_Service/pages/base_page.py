import logging
from typing import List

from selenium.webdriver import Keys, ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
import allure

from utils.ui.waitHelpers import WaitHelpers as WH

logger = logging.getLogger(__name__)


class BasePage:
    """Базовая страница с общими методами взаимодействия с элементами."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WH(self.driver)

    def open(self, url: str) -> None:
        """Открыть страницу по URL."""
        with allure.step(f"Открываем страницу по URL: {url}"):
            logger.info(f"Открываем страницу по URL: {url}")
            self.driver.get(url)

    def get_current_url(self) -> str:
        """Получить текущий URL страницы."""
        with allure.step("Получаем текущий URL страницы"):
            logger.info("Получаем текущий URL страницы")
            return self.driver.current_url

    def find_element(self, *locator) -> WebElement:
        """Поиск одного элемента по локатору."""
        with allure.step(f"Находим элемент с локатором: {locator}"):
            logger.info(f"Находим элемент с локатором: {locator}")
            element = self.wait.wait_for_element(locator)
            self.scroll(element)
            return element

    def find_elements(self, *locator) -> List[WebElement]:
        """Поиск всех элементов по локатору."""
        with allure.step(f"Находим все элементы с локатором: {locator}"):
            logger.info(f"Находим все элементы с локатором: {locator}")
            return self.driver.find_elements(*locator)

    def click(self, *locator) -> None:
        """Клик по элементу, найденному по локатору."""
        with allure.step(f"Кликаем по элементу с локатором: {locator}"):
            logger.info(f"Кликаем по элементу с локатором: {locator}")
            self.wait.wait_for_clickable(locator)
            element = self.find_element(*locator)
            try:
                element.click()
                return
            except ElementClickInterceptedException:
                logger.warning(
                    f"Клик по элементу {locator} перехвачен, прокручиваем и повторяем"
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", element
                )
            element = self.find_element(*locator)
            try:
                element.click()
            except ElementClickInterceptedException:
                logger.warning(
                    f"Клик по элементу {locator} перехвачен повторно, "
                    "выполняем JS-клик"
                )
                self.driver.execute_script("arguments[0].click();", element)

    def input_text(self, element: WebElement, text: str) -> None:
        """Ввести текст в поле."""
        with allure.step(f"Вводим текст '{text}' в элемент: {element}"):
            logger.info(f"Вводим текст '{text}' в элемент: {element}")
            element.clear()
            element.send_keys(text)

    def get_text(self, *locator) -> str:
        """Получить текст элемента."""
        with allure.step(f"Получаем текст элемента с локатором: {locator}"):
            logger.info(f"Получаем текст элемента с локатором: {locator}")
            return self.find_element(*locator).text.strip()

    def get_attribute_data(self, *locator, attribute: str) -> str:
        """Получить атрибут элемента."""
        with allure.step(f"Получаем атрибут '{attribute}' элемента с локатором: {locator}"):
            logger.info(f"Получаем атрибут '{attribute}' элемента с локатором: {locator}")
            return self.find_element(*locator).get_attribute(attribute)

    def is_element_displayed(self, *locator) -> bool:
        """Проверить, отображается ли элемент на странице."""
        with allure.step(f"Проверяем, отображается ли элемент с локатором: {locator}"):
            logger.info(f"Проверяем, отображается ли элемент с локатором: {locator}")
            elements = self.driver.find_elements(*locator)
            return bool(elements and elements[0].is_displayed())

    def scroll(self, element: WebElement):
        """Прокрутка страницы до указанного элемента."""
        with allure.step(f"Прокручиваем страницу до элемента: {element}"):
            logger.info(f"Прокручиваем страницу до элемента: {element}")
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", element
            )
        return self

    def press_escape(self) -> None:
        """Нажать клавишу Escape."""
        with allure.step("Нажимаем клавишу Escape"):
            logger.info("Нажимаем клавишу Escape")
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    def accept_alert(self) -> str:
        """Принять JS-alert и вернуть его текст."""
        with allure.step("Принимаем JS-alert и получаем его текст"):
            logger.info("Принимаем JS-alert и получаем его текст")
            alert = self.wait.wait_for_alert()
            text = alert.text
            alert.accept()
            return text