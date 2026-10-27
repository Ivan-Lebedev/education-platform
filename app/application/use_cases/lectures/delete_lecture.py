from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import LectureNotFoundError
from app.application.interfaces.unit_of_work import UnitOfWork


@dataclass(slots=True)
class DeleteLectureCommand:
    "Схема принимаемых данных для удаления сущности 'Лекция'."

    lecture_id: UUID


class DeleteLectureUseCase:
    "Сценарий удаления сущности 'Лекция'."

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: DeleteLectureCommand) -> None:
        async with self.uow:
            lecture = await self.uow.lectures.get_by_id(command.lecture_id)
            if lecture is None:
                raise LectureNotFoundError('Lecture not found.')

            section = await self.uow.sections.get_by_id(lecture.section_id)
            section.lecture_ids.remove(lecture.id)
            await self.uow.lectures.remove(command.lecture_id)
            await self.uow.commit()
