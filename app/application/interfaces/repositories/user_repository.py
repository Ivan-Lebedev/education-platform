from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.user import User


class UserRepository(ABC):
    "Контракт репозитория для сущности 'Пользователь'."

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        "Получение экземпляра пользователя по УИН при регистрации и входе в систему."

        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        "Извлечение экземпляра пользователя из bearer токена по электронной почте."

        raise NotImplementedError

    @abstractmethod
    async def add(self, user: User) -> None:
        "Добавление нового пользователя."

        raise NotImplementedError
