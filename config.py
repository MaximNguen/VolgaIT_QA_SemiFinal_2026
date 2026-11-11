#UI configs
IMPLICIT_WAIT_SECONDS = 10
AD_DISPLAY_TIMEOUT_SECONDS = 7

#Api configs
BASE_URL = "https://demoqa.com/swagger"
#Router User (reg and login)
ACCOUNT_PREFIX_URL = "/Account/v1/"
LOGIN_URL = "/GenerateToken"
REGISTER_URL = "/User"
CHECKUSER_URL = "/Authorized"

#Item books methods
ADD_URL = "/api/create"
GET_BOOK_URL = "/api/delete/"
GET_ALL_BOOKS_URL = "/api/getAll"
DELETE_BOOK_URL = "/api/get/"

TIMEOUT_SECONDS = 5

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}