from selenium.webdriver.common.by import By


class RegistrationPageLocators:
    """Класс локаторов для страницы регистрации"""
    
    register_header = (By.CSS_SELECTOR, "div.register-wrapper > h1")
    first_name_input = (By.ID, "firstname")
    last_name_input = (By.ID, "lastname")
    user_name_input = (By.ID, "userName")
    password_input = (By.ID, "password")
    submit_button = (By.ID, "register")
    error_message = (By.ID, "name")
    