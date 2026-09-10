import logging
import allure

from selenium.webdriver.support.ui import WebDriverWait

from UI_Service.pages.base_page import BasePage
from data.ui_data.locators_modals import ModalsPageLocators as MPL

logger = logging.getLogger(__name__)


class ModalsPage(BasePage):
    """Класс для взаимодействия со страницей «Модальные окна»."""

    def __init__(self, driver):
        super().__init__(driver)

    def click_simple_modal(self) -> None:
        """Клик по кнопке «Simple Modal»."""
        with allure.step("Кликаем по кнопке «Simple Modal»"):
            logger.info("Кликаем по кнопке «Simple Modal»")
            self.click(*MPL.simple_modal_button)

    def is_simple_modal_active(self) -> bool:
        """Проверить, открыто ли простое модальное окно."""
        with allure.step("Проверяем, открыто ли простое модальное окно"):
            logger.info("Проверяем, открыто ли простое модальное окно")
            # Элемент всегда в DOM (скрыт через display:none), поэтому
            # ищем по присутствию, а не по видимости.
            element = self.driver.find_element(*MPL.simple_popup)
            return "pum-active" in element.get_attribute("class")

    def wait_for_simple_modal(self) -> None:
        """Дождаться открытия простого модального окна."""
        with allure.step("Ожидаем открытия простого модального окна"):
            logger.info("Ожидаем открытия простого модального окна")
            self.wait.wait_until_class_contains(MPL.simple_popup, "pum-active")

    def get_simple_modal_title(self) -> str:
        """Получить заголовок простого модального окна."""
        with allure.step("Получаем заголовок простого модального окна"):
            logger.info("Получаем заголовок простого модального окна")
            return self.get_text(*MPL.simple_popup_title)

    def get_simple_modal_text(self) -> str:
        """Получить текст простого модального окна."""
        with allure.step("Получаем текст простого модального окна"):
            logger.info("Получаем текст простого модального окна")
            return self.get_text(*MPL.simple_popup_content)

    def close_simple_modal(self) -> None:
        """Закрыть простое модальное окно кнопкой «×»."""
        with allure.step("Закрываем простое модальное окно кнопкой «×»"):
            logger.info("Закрываем простое модальное окно кнопкой «×»")
            self.click(*MPL.simple_popup_close)
            WebDriverWait(self.driver, 5).until_not(
                lambda d: "pum-active" in d.find_element(*MPL.simple_popup).get_attribute("class")
            )

    def click_form_modal(self) -> None:
        """Клик по кнопке «Form Modal»."""
        with allure.step("Кликаем по кнопке «Form Modal»"):
            logger.info("Кликаем по кнопке «Form Modal»")
            self.click(*MPL.form_modal_button)

    def is_form_modal_active(self) -> bool:
        """Проверить, открыто ли модальное окно с формой."""
        with allure.step("Проверяем, открыто ли модальное окно с формой"):
            logger.info("Проверяем, открыто ли модальное окно с формой")
            element = self.driver.find_element(*MPL.form_popup)
            return "pum-active" in element.get_attribute("class")

    def wait_for_form_modal(self) -> None:
        """Дождаться открытия модального окна с формой."""
        with allure.step("Ожидаем открытия модального окна с формой"):
            logger.info("Ожидаем открытия модального окна с формой")
            self.wait.wait_until_class_contains(MPL.form_popup, "pum-active")

    def enter_name(self, text: str) -> None:
        """Ввести имя в поле Name."""
        with allure.step(f"Вводим имя '{text}' в поле Name"):
            logger.info(f"Вводим имя '{text}' в поле Name")
            self.input_text(self.find_element(*MPL.form_popup_name), text)

    def enter_email(self, text: str) -> None:
        """Ввести email в поле Email."""
        with allure.step(f"Вводим email '{text}' в поле Email"):
            logger.info(f"Вводим email '{text}' в поле Email")
            self.input_text(self.find_element(*MPL.form_popup_email), text)

    def enter_message(self, text: str) -> None:
        """Ввести сообщение в поле Message."""
        with allure.step(f"Вводим сообщение '{text}' в поле Message"):
            logger.info(f"Вводим сообщение '{text}' в поле Message")
            self.input_text(self.find_element(*MPL.form_popup_message), text)

    def click_submit(self) -> None:
        """Клик по кнопке Submit в модальном окне."""
        with allure.step("Кликаем по кнопке Submit"):
            logger.info("Кликаем по кнопке Submit")
            element = self.find_element(*MPL.form_popup_submit)
            # Кнопка находится внизу длинной формы. При появлении сообщения
            # валидации email макет сдвигается, и координатный клик перехватывается
            # другим элементом (ElementClickInterceptedException). Кликаем через JS,
            # чтобы запустить валидацию формы независимо от положения кнопки.
            self.driver.execute_script("arguments[0].click();", element)

    def get_name_error(self) -> str:
        """Получить текст ошибки поля Name."""
        with allure.step("Получаем текст ошибки поля Name"):
            logger.info("Получаем текст ошибки поля Name")
            return self.get_text(*MPL.form_popup_name_error)

    def get_email_error(self) -> str:
        """Получить текст ошибки поля Email."""
        with allure.step("Получаем текст ошибки поля Email"):
            logger.info("Получаем текст ошибки поля Email")
            return self.get_text(*MPL.form_popup_email_error)

    def get_form_errors_message(self) -> str:
        """Получить текст блока ошибок формы."""
        with allure.step("Получаем текст блока ошибок формы"):
            logger.info("Получаем текст блока ошибок формы")
            return self.get_text(*MPL.form_popup_errors_block)

    def is_form_errors_block_displayed(self) -> bool:
        """Проверить, отображается ли блок ошибок формы."""
        with allure.step("Проверяем, отображается ли блок ошибок формы"):
            logger.info("Проверяем, отображается ли блок ошибок формы")
            return self.is_element_displayed(*MPL.form_popup_errors_block)

    def is_success_displayed(self) -> bool:
        """Проверить, отображается ли блок успешной отправки."""
        with allure.step("Проверяем, отображается ли блок успешной отправки"):
            logger.info("Проверяем, отображается ли блок успешной отправки")
            return self.is_element_displayed(*MPL.form_popup_success)

    def get_success_message(self) -> str:
        """Получить текст сообщения об успехе."""
        with allure.step("Получаем текст сообщения об успехе"):
            logger.info("Получаем текст сообщения об успехе")
            return self.get_text(*MPL.form_popup_success_heading)

    def click_back(self) -> None:
        """Клик по кнопке «← Back»."""
        with allure.step("Кликаем по кнопке «← Back»"):
            logger.info("Кликаем по кнопке «← Back»")
            self.click(*MPL.form_popup_back)

    def close_form_modal(self) -> None:
        """Закрыть модальное окно с формой кнопкой «×»."""
        with allure.step("Закрываем модальное окно с формой кнопкой «×»"):
            logger.info("Закрываем модальное окно с формой кнопкой «×»")
            self.click(*MPL.form_popup_close)
            WebDriverWait(self.driver, 5).until_not(
                lambda d: "pum-active" in d.find_element(*MPL.form_popup).get_attribute("class")
            )
