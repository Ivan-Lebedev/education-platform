from abc import ABC, abstractmethod
from uuid import UUID


class TokenService(ABC):
    "Контракт сервиса по работе с токенами."

    @abstractmethod
    def create_access_token(self, user_id: UUID, role: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_user_id(self, token: str) -> UUID:
        raise NotImplementedError
