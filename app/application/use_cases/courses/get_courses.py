from dataclasses import dataclass

from app.application.interfaces.repositories import CourseRepository
from app.domain.entities import Course


@dataclass(slots=True)
class GetCoursesQuery:
    "Схема принимаемых данных для получения всех курсов."


class GetCoursesUseCase:
    "Сценарий получения всех курсов без вложенных сущностей."

    def __init__(self, course_repository: CourseRepository) -> None:
        self.course_repository = course_repository

    async def execute(self, query: GetCoursesQuery) -> list[Course]:
        return await self.course_repository.list()
