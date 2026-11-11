import logging

import allure
from typing import List

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

from UI_Service.pages.base_page import BasePage
from data.ui_data.locators_profile import ProfilePageLocators as PPL

logger = logging.getLogger(__name__)


class ProfilePage(BasePage):
    """Класс для взаимодействия со страницей профиля."""

    def __init__(self, driver):
        super().__init__(driver)

    def check_profile_header(self) -> bool:
        """Проверить, что заголовок страницы профиля загружен."""
        with allure.step("Проверим, что заголовок профиля загружен"):
            logger.info("Проверяем наличие заголовка профиля")
            return self.find_element(*PPL.profile_header).is_displayed()

    def goto_store(self) -> None:
        """Переход на страницу магазина."""
        with allure.step("Переходим на страницу магазина"):
            logger.info("Переходим на страницу магазина")
            self.click(*PPL.gotoShop)
            self.wait.wait_for_url_contains("/books")

    def get_table_books(self) -> WebElement:
        """Получить элемент таблицы книг в профиле."""
        with allure.step("Получаем элемент таблицы книг в профиле"):
            logger.info("Получаем элемент таблицы книг в профиле")
            return self.find_element(*PPL.book_list)

    def get_books_items(self) -> List[WebElement]:
        """Получить список строк таблицы книг на странице профиля."""
        with allure.step("Получаем строки таблицы книг в профиле"):
            logger.info("Получаем строки таблицы книг в профиле")
            table = self.get_table_books()
            return table.find_elements(By.CSS_SELECTOR, "tbody tr")

    def get_username(self) -> str:
        """Получить имя авторизованного пользователя."""
        with allure.step("Получаем имя пользователя из профиля"):
            logger.info("Получаем имя пользователя из профиля")
            return self.get_text(*PPL.user_name_value)

    def get_books(self, load_timeout: int = 0) -> list:
        """Получить список книг из профиля пользователя."""
        with allure.step("Получаем список книг из профиля"):
            logger.info("Получаем список книг из профиля")
            if load_timeout:
                try:
                    WebDriverWait(self.driver, load_timeout).until(
                        lambda driver: driver.find_elements(*PPL.book_rows)
                    )
                except TimeoutException:
                    pass
            self.find_element(*PPL.book_list)
            books = []
            for row in self.find_elements(*PPL.book_rows):
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

    def get_book_titles(self) -> list:
        """Получить названия книг из профиля пользователя."""
        with allure.step("Получаем названия книг из профиля"):
            logger.info("Получаем названия книг из профиля")
            return [book["title"] for book in self.get_books()]

    def wait_for_book(self, title: str, timeout: int = 10) -> None:
        """Дождаться появления книги в профиле."""
        with allure.step(f"Ожидаем появления книги в профиле: {title}"):
            logger.info(f"Ожидаем появления книги в профиле: {title}")
            locator = (By.XPATH, PPL.book_row_by_title.format(title=title))
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )

    def wait_for_book_absent(self, title: str, timeout: int = 10) -> None:
        """Дождаться исчезновения книги из профиля."""
        with allure.step(f"Ожидаем удаления книги из профиля: {title}"):
            logger.info(f"Ожидаем удаления книги из профиля: {title}")
            locator = (By.XPATH, PPL.book_row_by_title.format(title=title))
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )

    def delete_book(self, title: str) -> str:
        """Удалить книгу из профиля и вернуть текст alert."""
        with allure.step(f"Удаляем книгу из профиля: {title}"):
            logger.info(f"Удаляем книгу из профиля: {title}")
            locator = (By.XPATH, PPL.delete_book_by_title.format(title=title))
            self.click(*locator)
            self.click(*PPL.confirm_delete_ok)
            alert_text = self.accept_alert()
            self.wait_for_book_absent(title)
            return alert_text

    def logout(self) -> None:
        """Выйти из аккаунта."""
        with allure.step("Выходим из аккаунта"):
            logger.info("Выходим из аккаунта")
            self.click(*PPL.logout_button)
            self.wait.wait_for_url_contains("/login")
