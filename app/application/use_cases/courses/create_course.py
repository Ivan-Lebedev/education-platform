from dataclasses import dataclass
from uuid import uuid4

from app.application.exceptions import PermissionDeniedError
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities import Course, User


@dataclass(slots=True)
class CreateCourseCommand:
    "Схема принимаемых данных для создания экземпляра сущности 'Курс'."

    actor: User
    title: str
    description: str


class CreateCourseUseCase:
    "Сценарий создания экземпляра сущности 'Курс'."

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: CreateCourseCommand) -> Course:
        if not command.actor.can_manage_learning_content():
            raise PermissionDeniedError('User cannot create courses.')

        async with self.uow:
            course = Course(
                id=uuid4(),
                author_id=command.actor.id,
                title=command.title,
                description=command.description,
            )
            await self.uow.courses.add(course)
            await self.uow.commit()
            return course
