import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)


class WaitHelpers:
    """Класс утилит ожидания элементов."""

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator, timeout=10):
        """Ожидание видимости элемента."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException as e:
            logger.error(
                f"Элемент с локатором {locator} не найден за {timeout} секунд. - {e}"
            )

    def wait_for_clickable(self, locator, timeout=10):
        """Ожидание кликабельности элемента."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException as e:
            logger.error(
                f"Элемент с локатором {locator} не кликабелен за {timeout} секунд. - {e}"
            )

    def wait_for_page_load(self, timeout=3):
        """Ожидание полной загрузки страницы."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException as e:
            logger.error(f"Страница не загрузилась за {timeout} секунд. - {e}")
            return False

    def wait_until_class_contains(self, locator, expected_class, timeout=10):
        """Ожидание появления класса в атрибуте class элемента."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: expected_class in d.find_element(*locator).get_attribute("class")
            )
            return True
        except TimeoutException as e:
            logger.error(
                f"Класс '{expected_class}' не появился у элемента {locator} за {timeout} секунд. - {e}"
            )
            return False

    def wait_until_opacity(self, locator, expected_opacity="1", timeout=10):
        """Ожидание установки прозрачности элемента (завершение анимации появления)."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element(*locator).value_of_css_property("opacity")
                == expected_opacity
            )
            return True
        except TimeoutException as e:
            logger.error(
                f"Прозрачность {expected_opacity} не установлена у элемента {locator} "
                f"за {timeout} секунд. - {e}"
            )
            return False

    def wait_for_alert(self, timeout=10):
        """Ожидание появления JS-alert."""
        try:
            return WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        except TimeoutException as e:
            logger.error(f"Alert не появился за {timeout} секунд. - {e}")

    def wait_for_url_contains(self, fragment, timeout=10):
        """Ожидание появления фрагмента в текущем URL."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(fragment))
            return True
        except TimeoutException as e:
            logger.error(
                f"Фрагмент '{fragment}' не появился в URL за {timeout} секунд. - {e}"
            )
            return False

    def wait_for_element_absent(self, locator, timeout=10):
        """Ожидание исчезновения элемента со страницы."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException as e:
            logger.error(
                f"Элемент с локатором {locator} не исчез за {timeout} секунд. - {e}"
            )
            return False
