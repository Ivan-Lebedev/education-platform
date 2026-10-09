import os
from collections.abc import AsyncIterator
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import app.presentation.api.dependencies as api_dependencies
from app.infrastructure.database.models import (
    Base,
    CourseModel,
    LectureModel,
    ModuleModel,
    SectionModel,
    UserModel,
)
from app.infrastructure.security.password_hasher import PwdlibPasswordHasher
from app.main import create_app


@pytest_asyncio.fixture(scope='session')
async def test_engine(tmp_path_factory: pytest.TempPathFactory) -> AsyncIterator[AsyncEngine]:
    """
    Создаёт тестовую БД на всю тестовую сессию.

    С помощью встроенной фикстуры tmp_path_factory создает временную директорию pytest
    для изоляции от production-базы. База создаётся один раз на всю тестовую сессию.
    Все тесты используют одну БД, но изолируются через clear_database.
    Экономит время: не нужно создавать/удалять БД для каждого теста.

    До yield:
    - создание на диске файла тестовой БД;
    - создание отдельного async engine;
    - создание всех таблиц проекта.

    После yield:
    - удаление всех таблиц проекта;
    - закрытие пула соединений;
    - удаление файла тестовой БД с диска.

    Args:
        tmp_path_factory: Фабрика временных директорий pytest.

    Yields:
        AsyncEngine: Асинхронный движок SQLAlchemy для тестовой БД.
    """

    database_dir = tmp_path_factory.mktemp('test_db')
    database_path = Path(database_dir) / 'test_fastapi_education.db'
    database_url = f'sqlite+aiosqlite:///{database_path}'

    engine = create_async_engine(database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
    if database_path.exists():
        os.remove(database_path)


@pytest.fixture
def session_factory(test_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """
    Фабрика сессий для работы с тестовой базой данных.

    Создаёт новые асинхронные сессии SQLAlchemy, привязанные к тестовому движку.
    Используется для заполнения БД данными, очистки и подмены в зависимостях FastAPI.

    Args:
        test_engine: Тестовый движок SQLAlchemy.

    Returns:
        async_sessionmaker[AsyncSession]: Фабрика для создания асинхронных сессий.
    """

    return async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
    )


@pytest_asyncio.fixture
async def app(session_factory: async_sessionmaker[AsyncSession]) -> AsyncIterator[FastAPI]:
    """
    Создаёт FastAPI-приложение, подключённое к тестовой БД.

    Временно подменяет глобальную SessionFactory в зависимостях FastAPI на тестовую,
    чтобы приложение работало с тестовой БД вместо production.
    После завершения теста восстанавливает оригинальную фабрику.

    Args:
        session_factory: Тестовая фабрика асинхронных сессий.

    Yields:
        FastAPI: Тестовое приложение FastAPI.
    """

    app = create_app()
    original_session_factory = api_dependencies.SessionFactory
    api_dependencies.SessionFactory = session_factory
    try:
        yield app
    finally:
        api_dependencies.SessionFactory = original_session_factory


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    """
    Создаёт асинхронный HTTP-клиент для тестирования FastAPI-приложения.

    Использует ASGITransport для вызова FastAPI напрямую в памяти, без запуска реального
    uvicorn-сервера. Это ускоряет тесты, сохраняя настоящие HTTP-запросы и ответы.

    Args:
        app: Тестовое FastAPI-приложение.

    Yields:
        AsyncClient: HTTP-клиент httpx для отправки запросов к приложению.
    """

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        yield client


@pytest_asyncio.fixture(autouse=True)
async def clear_database(session_factory: async_sessionmaker[AsyncSession]) -> None:
    """
    Очищает тестовую БД перед каждым тестом для обеспечения изоляции.

    Запускается автоматически (autouse=True) перед каждым тестом.
    Удаляет данные из всех таблиц в правильном порядке (от дочерних к родительским
    для соблюдения ссылочной целостности) и гарантирует запуск каждого теста в чистой БД.

    Args:
        session_factory: Тестовая фабрика асинхронных сессий.
    """

    async with session_factory() as session:
        for model in [LectureModel, SectionModel, ModuleModel, CourseModel, UserModel]:
            await session.execute(delete(model))
        await session.commit()


@pytest_asyncio.fixture
async def seeded_course_tree(session_factory: async_sessionmaker[AsyncSession]) -> SimpleNamespace:
    """
    Создаёт минимальное дерево контента для тестов: курс → модуль → секция → лекция.

    Заполняет тестовую БД связанными сущностями и возвращает их идентификаторы
    и ожидаемые значения в компактном виде через SimpleNamespace.

    Args:
        session_factory: Тестовая фабрика асинхронных сессий.

    Returns:
        SimpleNamespace: Объект с идентификаторами и значениями созданного дерева.
    """

    course_id = str(uuid4())
    module_id = str(uuid4())
    section_id = str(uuid4())
    lecture_id = str(uuid4())

    async with session_factory() as session:
        course = CourseModel(
            id=course_id,
            title='FastAPI course',
            description='Clean architecture in practice.',
        )
        module = ModuleModel(
            id=module_id,
            course_id=course_id,
            title='MVP stage',
            description='Content, users and access.',
            position=1,
        )
        section = SectionModel(
            id=section_id,
            module_id=module_id,
            title='Auth section',
            description='JWT and route protection.',
            position=1,
        )
        lecture = LectureModel(
            id=lecture_id,
            section_id=section_id,
            title='Bearer token in practice',
            content='Lecture content',
            position=1,
        )
        session.add_all([course, module, section, lecture])
        await session.commit()

    return SimpleNamespace(
        course_id=course_id,
        module_id=module_id,
        section_id=section_id,
        lecture_id=lecture_id,
        course_title='FastAPI course',
        lecture_content='Lecture content',
    )


@pytest_asyncio.fixture
async def seeded_student_user(session_factory: async_sessionmaker[AsyncSession]) -> UserModel:
    """
    Создаёт тестового пользователя с ролью студента.

    Хеширует пароль через PwdlibPasswordHasher для совместимости
    с production-кодом аутентификации.

    Args:
        session_factory: Тестовая фабрика асинхронных сессий.

    Returns:
        UserModel: Созданная ORM-модель пользователя.
    """

    hasher = PwdlibPasswordHasher()
    async with session_factory() as session:
        user = UserModel(
            id=str(uuid4()),
            email='student@example.com',
            hashed_password=hasher.hash('strongpassword123'),
            role='student',
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest_asyncio.fixture
async def seeded_admin_user(session_factory: async_sessionmaker[AsyncSession]) -> UserModel:
    """
    Создаёт тестового пользователя с ролью администратора.

    Хеширует пароль через PwdlibPasswordHasher для совместимости
    с production-кодом аутентификации.

    Args:
        session_factory: Тестовая фабрика асинхронных сессий.

    Returns:
        UserModel: Созданная ORM-модель пользователя.
    """

    hasher = PwdlibPasswordHasher()
    async with session_factory() as session:
        user = UserModel(
            id=str(uuid4()),
            email='admin@example.com',
            hashed_password=hasher.hash('strongpassword123'),
            role='admin',
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@pytest_asyncio.fixture
async def student_auth_headers(
    client: AsyncClient, seeded_student_user: UserModel
) -> dict[str, str]:
    """
    Получает JWT-токен для студента и возвращает заголовки авторизации.

    Выполняет логин через API, извлекает access_token из ответа
    и формирует заголовок Authorization для защищённых эндпоинтов.

    Args:
        client: HTTP-клиент для запросов к API.
        seeded_student_user: Созданный пользователь-студент.

    Returns:
        dict: Словарь с заголовком Authorization для HTTP-запросов.
    """

    response = await client.post(
        '/api/auth/login',
        json={
            'email': 'student@example.com',
            'password': 'strongpassword123',
        },
    )
    token = response.json()['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest_asyncio.fixture
async def admin_auth_headers(client: AsyncClient, seeded_admin_user: UserModel) -> dict[str, str]:
    """
    Получает JWT-токен для администратора и возвращает заголовки авторизации.

    Выполняет логин через API, извлекает access_token из ответа
    и формирует заголовок Authorization для защищённых эндпоинтов.

    Args:
        client: HTTP-клиент для запросов к API.
        seeded_admin_user: Созданный пользователь-администратор.

    Returns:
        dict: Словарь с заголовком Authorization для HTTP-запросов.
    """

    response = await client.post(
        '/api/auth/login',
        json={
            'email': 'admin@example.com',
            'password': 'strongpassword123',
        },
    )
    token = response.json()['access_token']
    return {'Authorization': f'Bearer {token}'}
