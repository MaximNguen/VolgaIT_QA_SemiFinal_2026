# UI configs
IMPLICIT_WAIT_SECONDS = 10
AD_DISPLAY_TIMEOUT_SECONDS = 7

# API configs
BASE_URL = "https://demoqa.com"

# Account (registration, authorization)
REGISTER_URL = "/Account/v1/User"
LOGIN_URL = "/Account/v1/GenerateToken"
CHECKUSER_URL = "/Account/v1/Authorized"
USER_URL = "/Account/v1/User/"

# Book Store
GET_ALL_BOOKS_URL = "/BookStore/v1/Books"
ADD_BOOKS_URL = "/BookStore/v1/Books"
DELETE_BOOK_URL = "/BookStore/v1/Book"

TIMEOUT_SECONDS = 15

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}
