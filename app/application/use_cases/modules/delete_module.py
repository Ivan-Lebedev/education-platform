from dataclasses import dataclass
from uuid import UUID

from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.services.course_access_service import CourseAccessService
from app.application.use_cases.utils import delete_module_sections
from app.domain.entities import User


@dataclass(slots=True)
class DeleteModuleCommand:
    "Схема принимаемых данных для удаления сущности 'Модуль'."

    actor: User
    module_id: UUID


class DeleteModuleUseCase:
    "Сценарий удаления сущности 'Модуль'."

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.course_access_service = CourseAccessService(uow)

    async def execute(self, command: DeleteModuleCommand):
        async with self.uow:
            module = await self.course_access_service.ensure_can_manage_module(
                actor=command.actor,
                module_id=command.module_id,
            )

            await delete_module_sections(module=module, uow=self.uow)

            await self.uow.modules.remove(command.module_id)

            course = await self.uow.courses.get_by_id(module.course_id)
            if course is not None:
                course.remove_module(command.module_id)
                await self.uow.courses.update(course)

            await self.uow.commit()
