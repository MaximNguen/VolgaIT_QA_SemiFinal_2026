import logging
import os
import uuid

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest
import allure

from config import IMPLICIT_WAIT_SECONDS
from UI_Service.pages.factory_pages.page_factory import PageFactory
from data.ui_data.urls import account_api_url, login_page_url, profile_page_url

logger = logging.getLogger(__name__)


@pytest.fixture()
def driver():
    """Фикстура для создания драйвера Chrome с параметрами."""
    options = Options()
    # options.page_load_strategy = "eager"
    # options.add_argument("--headless")
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
def register_page(page_factory):
    """Фикстура для страницы регистрации."""
    return page_factory.register_page


@pytest.fixture
def login_page(page_factory):
    """Фикстура для страницы авторизации."""
    return page_factory.login_page


@pytest.fixture
def book_store_page(page_factory):
    """Фикстура для страницы магазина книг."""
    return page_factory.book_store_page


@pytest.fixture
def profile_page(page_factory):
    """Фикстура для страницы профиля."""
    return page_factory.profile_page


@pytest.fixture(scope="session")
def session_user():
    """Создаёт отдельного пользователя для каждого xdist-воркера."""
    worker = os.environ.get("PYTEST_XDIST_WORKER", "main")
    username = f"qa_{worker}_{uuid.uuid4().hex[:8]}"
    password = "Fodi2006@"
    response = requests.post(
        account_api_url,
        json={"userName": username, "password": password},
        timeout=30,
    )
    if response.status_code != 201:
        pytest.fail(
            "Не удалось создать тестового пользователя через API: "
            f"{response.status_code} {response.text}"
        )
    logger.info(f"Создан тестовый пользователь: {username}")
    return username, password


@pytest.fixture
def authorized_user(login_page, session_user):
    """Авторизует тестового пользователя и возвращает его логин и пароль."""
    username, password = session_user
    login_page.open(login_page_url)
    login_page.login(username, password)
    login_page.wait_until_logged_in()
    return username, password


@pytest.fixture
def empty_collection(profile_page, authorized_user):
    """Удаляет все книги из коллекции тестового пользователя."""
    profile_page.open(profile_page_url)
    for book in profile_page.get_books(load_timeout=2):
        profile_page.delete_book(book["title"])
    return authorized_user


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
