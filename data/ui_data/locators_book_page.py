from selenium.webdriver.common.by import By


class BookPageLocators:
    """Класс локаторов для страницы книг."""

    # Общая страница книг
    store_loaded = (By.ID, "searchBox")
    search_input = (By.ID, "searchBox")
    books_table = (By.CSS_SELECTOR, "div.books-wrapper table")
    books_rows = (By.CSS_SELECTOR, "div.books-wrapper table tbody tr")
    book_link_by_title = (
        '//div[contains(@class, "books-wrapper")]//a[normalize-space()="{title}"]'
    )

    # Страница конкретной книги
    detail_title = (By.XPATH, '//div[@id="title-wrapper"]//label[@id="userName-value"]')
    detail_author = (By.XPATH, '//div[@id="author-wrapper"]//label[@id="userName-value"]')
    detail_publisher = (By.XPATH, '//div[@id="publisher-wrapper"]//label[@id="userName-value"]')
    add_to_collection_button = (
        By.XPATH,
        '//button[normalize-space()="Add To Your Collection"]',
    )
    back_to_store_button = (
        By.XPATH,
        '//button[normalize-space()="Back To Book Store"]',
    )
