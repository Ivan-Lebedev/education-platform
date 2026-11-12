from abc import ABC, abstractmethod
from uuid import UUID


class QuestionAttemptRepository(ABC):
    "Контракт репозитория для сущности 'Попытка ответа на вопрос'."

    @abstractmethod
    async def exists_by_question_id(self, question_id: UUID) -> bool:
        raise NotImplementedError
