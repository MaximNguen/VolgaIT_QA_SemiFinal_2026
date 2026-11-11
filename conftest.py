import logging
import os
import uuid

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from api_Services.api.factory_endpoint.factory_endpoint import FactoryEndpoint
from api_Services.clients.book_client import BookClient
from api_Services.clients.user_client import UserClient
from config import IMPLICIT_WAIT_SECONDS
from UI_Service.pages.factory_pages.page_factory import PageFactory
from data.ui_data.urls import login_page_url, profile_page_url
from utils.api.payloads import build_user_payload

logger = logging.getLogger(__name__)


@pytest.fixture(params=["chrome", "firefox", "edge"])
def driver(request):
    """Фикстура для создания драйвера выбранного браузера."""
    browser_name = request.param

    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.page_load_strategy = "eager"
        driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        options.page_load_strategy = "eager"
        driver = webdriver.Firefox(options=options)
    elif browser_name == "edge":
        options = EdgeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.page_load_strategy = "eager"
        driver = webdriver.Edge(options=options)
    else:
        raise ValueError(
            f"Указан неверный браузер для тестирования: {browser_name}"
        )

    driver.set_page_load_timeout(60)
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
    payload = build_user_payload(username=username)
    user_client = UserClient()
    user = user_client.register(payload)
    logger.info(f"Создан тестовый пользователь: {user.username}")
    return user.username, payload["password"]


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


# ======================= Фикстуры для тестов API =======================


@pytest.fixture
def user_client():
    """Клиент Account API."""
    return UserClient()


@pytest.fixture
def book_client():
    """Клиент Book Store API."""
    return BookClient()


@pytest.fixture
def endpoint_factory():
    """Фабрика API-эндпоинтов."""
    factory = FactoryEndpoint()
    yield factory
    factory.clear_cache()


@pytest.fixture
def api_user(user_client):
    """Регистрирует пользователя через API и возвращает его данные."""
    payload = build_user_payload()
    user = user_client.register(payload)
    token_response = user_client.generate_token(payload)
    assert token_response.token, "Не получен токен авторизации"
    return {
        "payload": payload,
        "username": payload["userName"],
        "password": payload["password"],
        "userId": user.userID,
        "token": token_response.token,
    }


@pytest.fixture
def store_books(book_client):
    """Список книг магазина."""
    return book_client.get_store_books().books


@pytest.fixture
def api_clean_books(book_client, api_user):
    """Удаляет книги пользователя после теста."""
    yield
    try:
        book_client.delete_all_books(api_user["userId"], api_user["token"])
    except Exception as exc:
        logger.warning(f"Не удалось очистить коллекцию книг: {exc}")


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
