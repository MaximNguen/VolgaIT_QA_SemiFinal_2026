import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import allure

from utils.api.api_validators import (
    validate_add_books_request,
    validate_delete_book_request,
    validate_register_request,
)
from utils.api.generators import Generator

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
USER_PAYLOAD_PATH = REPO_ROOT / "data" / "api_data" / "user_payloads.json"
BOOK_PAYLOAD_PATH = REPO_ROOT / "data" / "api_data" / "book_payloads.json"


def _load_json(path: Path) -> Dict[str, Any]:
    """Загружает JSON-файл с тестовыми данными."""
    with allure.step(f"Загружаем тестовые данные из {path.name}"):
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as exc:
            logger.error(f"Ошибка при загрузке данных из {path}: {exc}")
            raise


@allure.step("Строим данные пользователя для API")
def build_user_payload(
    username: Optional[str] = None,
    password: Optional[str] = None,
    validate: bool = True,
) -> Dict[str, Any]:
    """Создаёт payload для регистрации/авторизации пользователя."""
    template = _load_json(USER_PAYLOAD_PATH)
    payload = {
        "userName": username or Generator.generate_username(),
        "password": password or template["password"],
    }
    if validate:
        validate_register_request(payload)
    return payload


@allure.step("Строим запрос добавления книг в коллекцию")
def build_add_books_payload(
    user_id: str,
    isbns: List[str],
) -> Dict[str, Any]:
    """Создаёт payload для добавления книг в коллекцию пользователя."""
    payload = {
        "userId": user_id,
        "collectionOfIsbns": [{"isbn": isbn} for isbn in isbns],
    }
    validate_add_books_request(payload)
    return payload


@allure.step("Строим запрос удаления книги из коллекции")
def build_delete_book_payload(user_id: str, isbn: str) -> Dict[str, Any]:
    """Создаёт payload для удаления книги из коллекции пользователя."""
    payload = {"isbn": isbn, "userId": user_id}
    validate_delete_book_request(payload)
    return payload


def get_wrong_password() -> str:
    """Возвращает неверный пароль для негативных тестов."""
    return _load_json(USER_PAYLOAD_PATH)["wrongPassword"]


def get_invalid_password() -> str:
    """Возвращает пароль, не подходящий под политику demoqa."""
    return _load_json(USER_PAYLOAD_PATH)["invalidPassword"]


def get_invalid_isbn() -> str:
    """Возвращает ISBN, которого нет в каталоге магазина."""
    return _load_json(BOOK_PAYLOAD_PATH)["invalidIsbn"]
