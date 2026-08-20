from dataclasses import dataclass
from uuid import uuid4

from app.application.interfaces.repositories import CourseRepository
from app.domain.entities import Course


@dataclass(slots=True)
class CreateCourseCommand:
    "Схема принимаемых данных для создания курса."

    title: str
    description: str


class CreateCourseUseCase:
    "Сценарий создания курса."

    def __init__(self, course_repository: CourseRepository) -> None:
        self.course_repository = course_repository

    async def execute(self, command: CreateCourseCommand) -> Course:
        course = Course(
            id=uuid4(),
            title=command.title,
            description=command.description,
        )
        await self.course_repository.add(course)
        return course
