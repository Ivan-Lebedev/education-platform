from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import ModuleNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.use_cases.utils import delete_module_sections


@dataclass(slots=True)
class DeleteModuleCommand:
    "Схема принимаемых данных для удаления сущности 'Модуль'."

    module_id: UUID


class DeleteModuleUseCase:
    "Сценарий удаления сущности 'Модуль'."

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: DeleteModuleCommand):
        async with self.uow:
            module = await self.uow.modules.get_by_id(command.module_id)
            if module is None:
                raise ModuleNotFoundError('Module not found.')

            await delete_module_sections(module=module, uow=self.uow)

            await self.uow.modules.remove(command.module_id)

            course = await self.uow.courses.get_by_id(module.course_id)
            if course is not None:
                course.remove_module(command.module_id)
                await self.uow.courses.update(course)

            await self.uow.commit()
