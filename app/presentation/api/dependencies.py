from collections.abc import AsyncIterator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.application.interfaces.services import PasswordHasher
from app.application.interfaces.services.token_service import TokenService
from app.application.use_cases import (
    CreateCourseUseCase,
    CreateLectureUseCase,
    CreateModuleUseCase,
    CreateSectionUseCase,
    GetCourseStructureUseCase,
    GetCoursesUseCase,
    GetCourseUseCase,
    GetLectureUseCase,
    LoginUserUseCase,
    RegisterUserUseCase,
    UpdateCourseUseCase,
    UpdateLectureUseCase,
    UpdateModuleUseCase,
    UpdateSectionUseCase,
)
from app.domain.entities import User
from app.infrastructure.database import SessionFactory, SqlAlchemyUnitOfWork
from app.infrastructure.security.jwt_token_service import InvalidTokenError, JwtTokenService
from app.infrastructure.security.password_hasher import PwdlibPasswordHasher
from app.presentation.exceptions import AuthenticationError


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


def get_password_hasher() -> PasswordHasher:
    "Провайдер зависимости, возвращающий сервис по работе с хешами паролей."

    return PwdlibPasswordHasher()


def get_token_service() -> TokenService:
    "Провайдер зависимости, возвращающий сервис по работе с JWT."

    return JwtTokenService()


def get_register_user_use_case() -> RegisterUserUseCase:
    "Провайдер зависимости, возвращающий сценарий регистрации пользователя."

    return RegisterUserUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory),
        password_hasher=get_password_hasher(),
    )


def get_login_user_use_case() -> LoginUserUseCase:
    "Провайдер зависимости, возвращающий сценарий логина пользователя."

    return LoginUserUseCase(
        uow=SqlAlchemyUnitOfWork(session_factory=SessionFactory),
        password_hasher=get_password_hasher(),
        token_service=get_token_service(),
    )


# auto_error=False т.к. необходимо явно контролировать, какую ошибку и в каком формате вернет API,
# при отсутствии или повреждении токена. Если оставить стандартное автоматическое поведение,
# часть auth-ошибок начнет обходить пользовательскую схему ErrorResponse и обработчики исключений.
http_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(http_bearer),
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
    token_service: TokenService = Depends(get_token_service),
) -> User:
    "Провайдер зависимости, возвращающий экземпляр пользователя, выполнившего запрос."

    if credentials is None:
        raise AuthenticationError('Authentication credentials were not provided.')

    if credentials.scheme.lower() != 'bearer':
        raise AuthenticationError('Authentication scheme must be Bearer.')

    try:
        user_id = token_service.get_user_id(credentials.credentials)
    except InvalidTokenError as exc:
        raise AuthenticationError(str(exc)) from exc

    user = await uow.users.get_by_id(user_id)
    if user is None:
        raise AuthenticationError('User from token was not found.')

    return user
