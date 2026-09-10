from selenium.webdriver.common.by import By


class AdsPageLocators:
    """Локаторы элементов страницы «Рекламные окна»."""

    countdown_text = (By.XPATH, "//p[contains(text(), 'An ad will appear in')]")
    popup = (By.ID, "pum-1272")
    popup_title = (By.CSS_SELECTOR, "#pum-1272 .pum-title")
    popup_content = (By.CSS_SELECTOR, "#pum-1272 .pum-content")
    popup_close = (By.CSS_SELECTOR, "#pum-1272 .pum-close")
    main_content = (By.CSS_SELECTOR, "main article")
