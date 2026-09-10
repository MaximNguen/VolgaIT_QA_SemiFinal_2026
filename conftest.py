import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest
import allure

from config import IMPLICIT_WAIT_SECONDS
from UI_Service.pages.factory_pages.page_factory import PageFactory

logger = logging.getLogger(__name__)


@pytest.fixture()
def driver():
    """Фикстура для создания драйвера Chrome с параметрами."""
    options = Options()
    options.page_load_strategy = "eager"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(IMPLICIT_WAIT_SECONDS)

    yield driver

    driver.quit()


@pytest.fixture
def page_factory(driver):
    """Фикстура для фабрики страниц."""
    return PageFactory(driver)


@pytest.fixture
def calendar_page(page_factory):
    """Фикстура для страницы календаря."""
    return page_factory.calendar_page


@pytest.fixture
def modals_page(page_factory):
    """Фикстура для страницы модальных окон."""
    return page_factory.modals_page


@pytest.fixture
def ads_page(page_factory):
    """Фикстура для страницы рекламных окон."""
    return page_factory.ads_page


@pytest.fixture
def form_fields_page(page_factory):
    """Фикстура для страницы формы."""
    return page_factory.form_fields_page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """При падении теста прикрепляет скриншот Selenium к Allure-отчёту."""
    outcome = yield
    report = outcome.get_result()

    if not report.failed or getattr(report, "wasxfail", False):
        return

    driver = item.funcargs.get("driver")
    if driver is None:
        return

    try:
        screenshot = driver.get_screenshot_as_png()
    except Exception:
        return

    allure.attach(
        screenshot,
        name=f"{item.name}_{report.when}",
        attachment_type=allure.attachment_type.PNG,
    )
