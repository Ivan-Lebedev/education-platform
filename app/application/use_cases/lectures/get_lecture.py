from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import LectureNotFoundError
from app.application.interfaces.repositories import LectureRepository
from app.domain.entities import Lecture


@dataclass(slots=True)
class GetLectureQuery:
    "Схема принимаемых данных для получения лекции."

    lecture_id: UUID


class GetLectureUseCase:
    "Сценарий получения лекции."

    def __init__(self, lecture_repository: LectureRepository) -> None:
        self.lecture_repository = lecture_repository

    async def execute(self, query: GetLectureQuery) -> Lecture:
        lecture = await self.lecture_repository.get_by_id(query.lecture_id)
        if lecture is None:
            raise LectureNotFoundError('Lecture not found.')
        return lecture
