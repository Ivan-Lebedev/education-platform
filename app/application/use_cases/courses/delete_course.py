from dataclasses import dataclass
from uuid import UUID

from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.course_access_service import CourseAccessService
from app.application.use_cases.utils import delete_course_modules
from app.domain.entities import User


@dataclass(slots=True)
class DeleteCourseCommand:
    "Схема принимаемых данных для удаления сущности 'Курс'."

    actor: User
    course_id: UUID


class DeleteCourseUseCase:
    "Сценарий удаления сущности 'Курс'."

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.course_access_service = CourseAccessService(uow)

    async def execute(self, command: DeleteCourseCommand):
        async with self.uow:
            course = await self.course_access_service.ensure_can_manage_course(
                actor=command.actor, course_id=command.course_id
            )

            await delete_course_modules(course, self.uow)

            await self.uow.courses.remove(command.course_id)

            await self.uow.commit()
