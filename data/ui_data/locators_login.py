from selenium.webdriver.common.by import By


class LoginPageLocators:
    """Класс локаторов для страницы авторизации."""

    login_header = (By.CSS_SELECTOR, "div.login-wrapper > h1")
    username_input = (By.ID, "userName")
    password_input = (By.ID, "password")
    login_button = (By.ID, "login")
    error_message = (By.ID, "name")