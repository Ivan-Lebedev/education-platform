from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.user import User


class UserRepository(ABC):
    "Контракт репозитория для сущности 'Пользователь'."

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        "Метод получения экземпляра пользователя по УИН при регистрации и логине."

        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        "Метод для извлечения экземпляра пользователя из bearer токена по электронной почте."

        raise NotImplementedError

    @abstractmethod
    async def add(self, user: User) -> None:
        "Метод для сохранения нового пользователя."

        raise NotImplementedError
