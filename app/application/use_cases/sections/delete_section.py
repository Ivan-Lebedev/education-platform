from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import SectionNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork


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

            module = await self.uow.modules.get_by_id(section.module_id)
            if module:
                module.remove_section(command.section_id)
                await self.uow.modules.update(module)
            lectures = await self.uow.lectures.get_by_ids(section.lecture_ids)
            for lecture in lectures:
                await self.uow.lectures.delete(lecture.id)
            await self.uow.sections.delete(command.section_id)
            await self.uow.commit()
