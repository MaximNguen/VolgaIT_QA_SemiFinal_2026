import logging
from typing import Dict, Literal, Optional, overload

from api_Services.api.add_books_endpoint import AddBooksEndpoint
from api_Services.api.authorized_user_endpoint import AuthorizedUserEndpoint
from api_Services.api.base_endpoint import BaseEndpoint
from api_Services.api.delete_book_endpoint import DeleteBookEndpoint
from api_Services.api.get_profile_books_endpoint import (
    GetProfileBooksEndpoint,
)
from api_Services.api.get_store_books_endpoint import GetStoreBooksEndpoint
from api_Services.api.login_user_endpoint import LoginUserEndpoint
from api_Services.api.register_user_endpoint import RegisterUserEndpoint

logger = logging.getLogger(__name__)


class FactoryEndpoint:
    """Фабрика для создания экземпляров эндпоинтов."""

    EndpointName = Literal[
        "register",
        "login",
        "authorize",
        "get_store_books",
        "add_books",
        "delete_book",
        "get_profile_books",
    ]
    ENDPOINT_CLASSES = {
        "register": RegisterUserEndpoint,
        "login": LoginUserEndpoint,
        "authorize": AuthorizedUserEndpoint,
        "get_store_books": GetStoreBooksEndpoint,
        "add_books": AddBooksEndpoint,
        "delete_book": DeleteBookEndpoint,
        "get_profile_books": GetProfileBooksEndpoint,
    }

    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = base_url
        self._cache: Dict[FactoryEndpoint.EndpointName, BaseEndpoint] = {}

    @overload
    def get(self, name: Literal["register"]) -> RegisterUserEndpoint:
        ...

    @overload
    def get(self, name: Literal["login"]) -> LoginUserEndpoint:
        ...

    @overload
    def get(self, name: Literal["authorize"]) -> AuthorizedUserEndpoint:
        ...

    @overload
    def get(
        self,
        name: Literal["get_store_books"],
    ) -> GetStoreBooksEndpoint:
        ...

    @overload
    def get(self, name: Literal["add_books"]) -> AddBooksEndpoint:
        ...

    @overload
    def get(self, name: Literal["delete_book"]) -> DeleteBookEndpoint:
        ...

    @overload
    def get(
        self,
        name: Literal["get_profile_books"],
    ) -> GetProfileBooksEndpoint:
        ...

    def get(self, name: EndpointName) -> BaseEndpoint:
        endpoint_class = self.ENDPOINT_CLASSES[name]
        if name not in self._cache:
            self._cache[name] = (
                endpoint_class(self.base_url)
                if self.base_url
                else endpoint_class()
            )
        return self._cache[name]

    def clear_cache(self) -> None:
        """Очищает кэш созданных эндпоинтов."""
        self._cache.clear()
