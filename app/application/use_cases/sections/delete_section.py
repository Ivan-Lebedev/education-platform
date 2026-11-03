from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import SectionNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.use_cases.utils import delete_section_lectures


@dataclass(slots=True)
class DeleteSectionCommand:
    "Схема принимаемых данных для удаления сущности 'Раздел'."

    section_id: UUID


class DeleteSectionUseCase:
    "Сценарий удаления сущности 'Раздел'."

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: DeleteSectionCommand) -> None:
        async with self.uow:
            section = await self.uow.sections.get_by_id(command.section_id)
            if section is None:
                raise SectionNotFoundError('Section not found.')

            await delete_section_lectures(section=section, uow=self.uow)

            await self.uow.sections.remove(command.section_id)

            module = await self.uow.modules.get_by_id(section.module_id)
            if module:
                module.remove_section(command.section_id)
                await self.uow.modules.update(module)

            await self.uow.commit()
