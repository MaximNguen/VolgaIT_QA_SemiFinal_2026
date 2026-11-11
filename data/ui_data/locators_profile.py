from selenium.webdriver.common.by import By


class ProfilePageLocators:
    """Класс локаторов для страницы профиля."""

    profile_header = (By.XPATH, '//*[@id="userName-label"]')
    user_name_value = (By.ID, "userName-value")
    logout_button = (By.XPATH, '//button[normalize-space()="Logout"]')
    book_list = (By.CSS_SELECTOR, "div.profile-wrapper table")
    book_rows = (By.CSS_SELECTOR, "div.profile-wrapper table tbody tr")
    book_titles = (By.CSS_SELECTOR, "div.profile-wrapper table tbody tr a")
    book_row_by_title = (
        '//div[contains(@class, "profile-wrapper")]'
        '//tr[.//a[normalize-space()="{title}"]]'
    )
    delete_book_by_title = (
        '//div[contains(@class, "profile-wrapper")]'
        '//tr[.//a[normalize-space()="{title}"]]'
        '//span[starts-with(@id, "delete-record-")]/svg'
    )
    confirm_delete_ok = (By.ID, "closeSmallModal-ok")
    confirm_delete_cancel = (By.ID, "closeSmallModal-cancel")

    gotoShop = (By.ID, "gotoStore")
