from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import CourseNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.use_cases.utils import delete_course_modules


@dataclass(slots=True)
class DeleteCourseCommand:
    "Схема принимаемых данных для удаления сущности 'Курс'."

    course_id: UUID


class DeleteCourseUseCase:
    "Сценарий удаления сущности 'Курс'."

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: DeleteCourseCommand):
        async with self.uow:
            course = await self.uow.courses.get_by_id(command.course_id)
            if course is None:
                raise CourseNotFoundError('Course not found.')

            await delete_course_modules(course, self.uow)

            await self.uow.courses.delete(command.course_id)

            await self.uow.commit()
