from selenium.webdriver.common.by import By


class FormFieldsPageLocators:
    """Локаторы элементов страницы «Форма»."""

    form = (By.ID, "feedbackForm")
    name_input = (By.ID, "name-input")
    message_input = (By.ID, "message")
    submit_button = (By.ID, "submit-btn")
    automation_tools_label = (
        By.XPATH,
        "//form[@id='feedbackForm']/label[normalize-space()='Automation tools']",
    )
    automation_tools_items = (
        By.XPATH,
        "//form[@id='feedbackForm']/label[normalize-space()='Automation tools']/following-sibling::ul[1]/li",
    )
