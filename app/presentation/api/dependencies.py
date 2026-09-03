from collections.abc import AsyncIterator

from fastapi import Depends

from app.application.use_cases import (
    GetCourseStructureUseCase,
    GetCoursesUseCase,
    GetCourseUseCase,
    GetLectureUseCase,
)
from app.infrastructure.database import SessionFactory, SqlAlchemyUnitOfWork


async def get_uow() -> AsyncIterator[SqlAlchemyUnitOfWork]:
    """
    Асинхронный генератор, создающий объект 'SqlAlchemyUnitOfWork' с фабрикой сессий.

    Используется как вспомогательная зависимость для зависимостей получения
    сценариев взаимодействия при обработке маршрутов через Depends (DI).
    """

    async with SqlAlchemyUnitOfWork(session_factory=SessionFactory) as uow:
        yield uow


def get_get_courses_use_case(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetCoursesUseCase:
    "Провайдер зависимости, возвращающий сценарий получения списка курсов."

    return GetCoursesUseCase(course_repository=uow.courses)


def get_get_course_use_case(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetCourseUseCase:
    "Провайдер зависимости, возвращающий сценарий получения курса."

    return GetCourseUseCase(course_repository=uow.courses)


def get_get_course_structure_use_case(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetCourseStructureUseCase:
    "Провайдер зависимости, возвращающий сценарий получения полной структуры курса."

    return GetCourseStructureUseCase(
        course_repository=uow.courses,
        module_repository=uow.modules,
        section_repository=uow.sections,
        lecture_repository=uow.lectures,
    )


def get_get_lecture_use_case(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetLectureUseCase:
    "Провайдер зависимости, возвращающий сценарий получения лекции."

    return GetLectureUseCase(lecture_repository=uow.lectures)
