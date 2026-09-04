from collections.abc import AsyncIterator

from fastapi import Depends

from app.application.use_cases import (
    CreateCourseUseCase,
    CreateLectureUseCase,
    CreateModuleUseCase,
    CreateSectionUseCase,
    GetCourseStructureUseCase,
    GetCoursesUseCase,
    GetCourseUseCase,
    GetLectureUseCase,
    UpdateCourseUseCase,
    UpdateLectureUseCase,
    UpdateModuleUseCase,
    UpdateSectionUseCase,
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


def get_get_courses_use_case(uow: SqlAlchemyUnitOfWork = Depends(get_uow)) -> GetCoursesUseCase:
    "Провайдер зависимости, возвращающий сценарий получения списка курсов."

    return GetCoursesUseCase(course_repository=uow.courses)


def get_get_course_use_case(uow: SqlAlchemyUnitOfWork = Depends(get_uow)) -> GetCourseUseCase:
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


def get_get_lecture_use_case(uow: SqlAlchemyUnitOfWork = Depends(get_uow)) -> GetLectureUseCase:
    "Провайдер зависимости, возвращающий сценарий получения лекции из раздела модуля курса."

    return GetLectureUseCase(lecture_repository=uow.lectures)


def get_create_course_use_case() -> CreateCourseUseCase:
    "Провайдер зависимости, возвращающий сценарий создания курса."

    return CreateCourseUseCase(uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory))


def get_update_course_use_case() -> UpdateCourseUseCase:
    "Провайдер зависимости, возвращающий сценарий обновления курса."

    return UpdateCourseUseCase(uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory))


def get_create_module_use_case() -> CreateModuleUseCase:
    "Провайдер зависимости, возвращающий сценарий создания модуля курса."

    return CreateModuleUseCase(uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory))


def get_update_module_use_case() -> UpdateModuleUseCase:
    "Провайдер зависимости, возвращающий сценарий обновления модуля курса."

    return UpdateModuleUseCase(uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory))


def get_create_section_use_case() -> CreateSectionUseCase:
    "Провайдер зависимости, возвращающий сценарий создания раздела из модуля курса."

    return CreateSectionUseCase(uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory))


def get_update_section_use_case() -> UpdateSectionUseCase:
    "Провайдер зависимости, возвращающий сценарий обновления раздела из модуля курса."

    return UpdateSectionUseCase(uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory))


def get_create_lecture_use_case() -> CreateLectureUseCase:
    "Провайдер зависимости, возвращающий сценарий создания лекции из раздела модуля курса."

    return CreateLectureUseCase(uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory))


def get_update_lecture_use_case() -> UpdateLectureUseCase:
    "Провайдер зависимости, возвращающий сценарий обновления лекции из раздела модуля курса."

    return UpdateLectureUseCase(uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory))
