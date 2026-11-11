from selenium.webdriver.common.by import By


class ProfilePageLocators:
    """Класс локаторов для страницы профиля."""

    profile_header = (By.XPATH, '//*[@id="userName-label"]')
    logout_button = (By.ID, "submit")
    book_list = (By.CSS_SELECTOR, "div.profile-wrapper > div:nth-child(2) > table")
    book_element = (By.CSS_SELECTOR, "div.profile-wrapper > div:nth-child(2) > table > tbody > tr")
    
    gotoShop = (By.ID, "gotoStore")