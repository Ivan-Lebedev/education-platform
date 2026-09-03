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
    "Зависимость для получения объекта 'UnitOfWork'."

    async with SqlAlchemyUnitOfWork(session_factory=SessionFactory) as uow:
        yield uow


def get_get_courses_use_case(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetCoursesUseCase:
    "Зависимость для получения сценария получения списка курсов."

    return GetCoursesUseCase(course_repository=uow.courses)


def get_get_course_use_case(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetCourseUseCase:
    "Зависимость для получения сценария получения курса."

    return GetCourseUseCase(course_repository=uow.courses)


def get_get_course_structure_use_case(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetCourseStructureUseCase:
    "Зависимость для получения сценария получения структуры курса."

    return GetCourseStructureUseCase(
        course_repository=uow.courses,
        module_repository=uow.modules,
        section_repository=uow.sections,
        lecture_repository=uow.lectures,
    )


def get_get_lecture_use_case(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
) -> GetLectureUseCase:
    "Зависимость для получения лекции."

    return GetLectureUseCase(lecture_repository=uow.lectures)
