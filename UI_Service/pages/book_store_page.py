import logging

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from UI_Service.pages.base_page import BasePage
from data.ui_data.locators_book_page import BookPageLocators as BPL

logger = logging.getLogger(__name__)


class BookStorePage(BasePage):
    """Класс для взаимодействия со страницей магазина книг."""

    def __init__(self, driver):
        super().__init__(driver)

    def check_store_loaded(self) -> bool:
        """Проверить, что страница магазина загружена."""
        with allure.step("Проверяем, что страница магазина загружена"):
            logger.info("Проверяем, что страница магазина загружена")
            return self.find_element(*BPL.store_loaded).is_displayed()

    def get_books(self) -> list:
        """Получить список книг магазина."""
        with allure.step("Получаем список книг магазина"):
            logger.info("Получаем список книг магазина")
            self.find_element(*BPL.books_rows)
            books = []
            for row in self.find_elements(*BPL.books_rows):
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) < 4:
                    continue
                links = row.find_elements(By.CSS_SELECTOR, "a")
                if not links:
                    continue
                books.append(
                    {
                        "title": links[0].text.strip(),
                        "author": cells[2].text.strip(),
                        "publisher": cells[3].text.strip(),
                    }
                )
            return books
        
    def check_search_input(self) -> bool:
        """Проверка отображаемости поля поиска."""
        with allure.step("Проверяем наличие поля поиска"):
            logger.info("Проверяем наличие поля поиска")
            return self.find_element(*BPL.search_input).is_displayed()

    def get_search_input(self) -> WebElement:
        """Получить поле поиска."""
        with allure.step("Получаем поле поиска"):
            logger.info("Получаем поле поиска")
            return self.find_element(*BPL.search_input)

    def input_search_text(self, text: str) -> None:
        """Ввести текст в поле поиска."""
        with allure.step(f"Вводим текст - {text} в поле поиска"):
            logger.info(f"Вводим текст - {text} в поле поиска")
            self.input_text(self.get_search_input(), text)

    def search_books(self, text: str, timeout: int = 10) -> None:
        """Ввести поисковый запрос и дождаться фильтрации книг."""
        with allure.step(f"Ищем книги по запросу: {text}"):
            logger.info(f"Ищем книги по запросу: {text}")
            self.input_search_text(text)

            def books_filtered(driver):
                titles = [
                    link.text.strip()
                    for link in driver.find_elements(*BPL.book_title_links)
                ]
                if titles:
                    return all(
                        text.lower() in title.lower() for title in titles
                    )
                value = driver.find_element(*BPL.search_input).get_attribute(
                    "value"
                )
                return value == text

            WebDriverWait(self.driver, timeout).until(books_filtered)

    def get_search_result_titles(self) -> list:
        """Получить названия книг, отфильтрованных поиском."""
        with allure.step("Получаем результаты поиска книг"):
            logger.info("Получаем результаты поиска книг")
            return [
                link.text.strip()
                for link in self.find_elements(*BPL.book_title_links)
            ]

    def get_book_titles(self) -> list:
        """Получить список названий книг магазина."""
        with allure.step("Получаем названия книг магазина"):
            logger.info("Получаем названия книг магазина")
            return [book["title"] for book in self.get_books()]

    def open_book(self, title: str) -> None:
        """Открыть страницу книги по её названию."""
        with allure.step(f"Открываем страницу книги: {title}"):
            logger.info(f"Открываем страницу книги: {title}")
            locator = (By.XPATH, BPL.book_link_by_title.format(title=title))
            self.click(*locator)
            self.wait.wait_for_url_contains("/books?search=")
            self.find_element(*BPL.detail_title)

    def add_book_to_collection(self) -> str:
        """Добавить открытую книгу в коллекцию пользователя и вернуть текст alert."""
        with allure.step("Добавляем книгу в коллекцию пользователя"):
            logger.info("Добавляем книгу в коллекцию пользователя")
            self.click(*BPL.add_to_collection_button)
            return self.accept_alert()

    def back_to_store(self) -> None:
        """Вернуться со страницы книги в магазин."""
        with allure.step("Возвращаемся в магазин книг"):
            logger.info("Возвращаемся в магазин книг")
            self.click(*BPL.back_to_store_button)
            self.find_element(*BPL.books_rows)
