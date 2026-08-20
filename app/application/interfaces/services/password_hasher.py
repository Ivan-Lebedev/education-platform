from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    "Контракт сервиса работы с хешами."

    @abstractmethod
    def hash(self, raw_password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify(self, raw_password: str, hashed_password: str) -> bool:
        raise NotImplementedError
