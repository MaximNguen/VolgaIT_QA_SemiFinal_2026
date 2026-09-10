from selenium.webdriver.common.by import By


class ModalsPageLocators:
    """Локаторы элементов страницы «Модальные окна»."""

    simple_modal_button = (By.XPATH, "//button[normalize-space()='Simple Modal']")
    form_modal_button = (By.XPATH, "//button[normalize-space()='Form Modal']")

    simple_popup = (By.ID, "pum-1318")
    simple_popup_title = (By.CSS_SELECTOR, "#pum-1318 .pum-title")
    simple_popup_content = (By.CSS_SELECTOR, "#pum-1318 .pum-content")
    simple_popup_close = (By.CSS_SELECTOR, "#pum-1318 .pum-close")

    form_popup = (By.ID, "pum-674")
    form_popup_name = (By.ID, "g1051-name")
    form_popup_email = (By.ID, "g1051-email")
    form_popup_message = (By.ID, "contact-form-comment-g1051-message")
    form_popup_submit = (By.CSS_SELECTOR, "#pum-674 button.pushbutton-wide")
    form_popup_close = (By.CSS_SELECTOR, "#pum-674 .pum-close")
    form_popup_name_error = (By.ID, "g1051-name-text-error")
    form_popup_email_error = (By.ID, "g1051-email-email-error")
    form_popup_errors_block = (By.CSS_SELECTOR, "#pum-674 .contact-form__error.show-errors")
    form_popup_success = (By.CSS_SELECTOR, "#pum-674 .contact-form-submission.submission-success")
    form_popup_success_heading = (By.CSS_SELECTOR, "#pum-674 .contact-form-submission.submission-success h4")
    form_popup_back = (By.CSS_SELECTOR, "#pum-674 .go-back-message a")
