import logging
import random
import string

logger = logging.getLogger(__name__)


class Generator:
    """Класс для генерации случайных данных для тестов."""

    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """Генерирует случайную строку заданной длины."""
        logger.info(f"Генерируем случайную строку длиной {length}")
        characters = string.ascii_letters + string.digits
        return "".join(random.choices(characters, k=length))

    @staticmethod
    def generate_username(prefix: str = "qa") -> str:
        """Генерирует уникальный username для регистрации."""
        return f"{prefix}{Generator.generate_random_string(10)}"
