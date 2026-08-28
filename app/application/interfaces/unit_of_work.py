from abc import ABC, abstractmethod
from types import TracebackType

from .repositories import (
    CourseRepository,
    LectureRepository,
    ModuleRepository,
    SectionRepository,
)


class UnitOfWork(ABC):
    "Контракт для объекта 'UnitOfWork'."

    courses: CourseRepository
    modules: ModuleRepository
    sections: SectionRepository
    lectures: LectureRepository

    @abstractmethod
    async def __aenter__(self) -> 'UnitOfWork':
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
