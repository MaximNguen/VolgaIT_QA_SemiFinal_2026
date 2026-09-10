import logging
from selenium.webdriver.remote.webdriver import WebDriver

from UI_Service.pages.calendar_page import CalendarPage
from UI_Service.pages.modals_page import ModalsPage
from UI_Service.pages.ads_page import AdsPage
from UI_Service.pages.form_fields_page import FormFieldsPage

logger = logging.getLogger(__name__)


class PageFactory:
    """Фабрика для создания и управления страницами. Паттерн Factory."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.pages_data = {
            "calendar_page": CalendarPage(self.driver),
            "modals_page": ModalsPage(self.driver),
            "ads_page": AdsPage(self.driver),
            "form_fields_page": FormFieldsPage(self.driver),
        }

    def get_page(self, page_name: str) -> object:
        """Получить страницу по имени."""
        if page_name in self.pages_data:
            logger.info(f"Страница '{page_name}' найдена в фабрике.")
            return self.pages_data[page_name]
        logger.error(f"Страница '{page_name}' не найдена в фабрике.")
        raise ValueError(f"Страница '{page_name}' не найдена в фабрике.")

    @property
    def calendar_page(self) -> CalendarPage:
        """Получить страницу календаря."""
        return self.get_page("calendar_page")

    @property
    def modals_page(self) -> ModalsPage:
        """Получить страницу модальных окон."""
        return self.get_page("modals_page")

    @property
    def ads_page(self) -> AdsPage:
        """Получить страницу рекламных окон."""
        return self.get_page("ads_page")

    @property
    def form_fields_page(self) -> FormFieldsPage:
        """Получить страницу формы."""
        return self.get_page("form_fields_page")
