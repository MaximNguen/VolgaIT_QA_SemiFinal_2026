from selenium.webdriver.common.by import By


class CalendarPageLocators:
    """Локаторы элементов страницы «Календарь»."""

    heading = (By.CSS_SELECTOR, "h1")
    form = (By.ID, "contact-form-1065-1")
    date_input = (By.ID, "g1065-1-selectorenteradate")
    submit_button = (By.CSS_SELECTOR, "button.pushbutton-wide")
    date_error_message = (By.ID, "g1065-1-selectorenteradate-text-error-message")
    form_errors_block = (By.CSS_SELECTOR, ".contact-form__error.show-errors")
    success_block = (By.CSS_SELECTOR, ".contact-form-submission.submission-success")
    success_heading = (By.CSS_SELECTOR, ".contact-form-submission.submission-success h4")
    success_summary = (By.CSS_SELECTOR, ".jetpack_forms_contact-form-success-summary")
    back_button = (By.CSS_SELECTOR, ".contact-form-submission.submission-success .go-back-message a")
