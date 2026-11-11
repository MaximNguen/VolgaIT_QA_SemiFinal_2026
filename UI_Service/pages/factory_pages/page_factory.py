import logging
from selenium.webdriver.remote.webdriver import WebDriver

from UI_Service.pages.register_page import RegisterPage
from UI_Service.pages.login_page import LoginPage
from UI_Service.pages.book_store_page import BookStorePage
from UI_Service.pages.profile_page import ProfilePage

logger = logging.getLogger(__name__)


class PageFactory:
    """Фабрика для создания и управления страницами. Паттерн Factory."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.pages_data = {
            "register_page": RegisterPage(self.driver),
            "login_page": LoginPage(self.driver),
            "book_store_page": BookStorePage(self.driver),
            "profile_page": ProfilePage(self.driver),
        }

    def get_page(self, page_name: str) -> object:
        """Получить страницу по имени."""
        if page_name in self.pages_data:
            logger.info(f"Страница '{page_name}' найдена в фабрике.")
            return self.pages_data[page_name]
        logger.error(f"Страница '{page_name}' не найдена в фабрике.")
        raise ValueError(f"Страница '{page_name}' не найдена в фабрике.")

    @property
    def register_page(self) -> RegisterPage:
        """Получить страницу регистрации."""
        return self.get_page("register_page")

    @property
    def login_page(self) -> LoginPage:
        """Получить страницу логина."""
        return self.get_page("login_page")

    @property
    def book_store_page(self) -> BookStorePage:
        """Получить страницу магазина книг."""
        return self.get_page("book_store_page")

    @property
    def profile_page(self) -> ProfilePage:
        """Получить страницу профиля."""
        return self.get_page("profile_page")
