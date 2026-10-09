from types import SimpleNamespace
from uuid import uuid4

from httpx import AsyncClient


async def test_get_courses_returns_public_list(
    client: AsyncClient, seeded_course_tree: SimpleNamespace
) -> None:
    """
    Сценарий проверки получения списка курсов.

    Проверяет, что маршрут возвращает статус-код 200 и список, содержащий
    только один созданный курс с ожидаемым названием.
    """

    response = await client.get('/api/courses')

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]['title'] == seeded_course_tree.course_title


async def test_get_course_returns_single_course(
    client: AsyncClient, seeded_course_tree: SimpleNamespace
) -> None:
    """
    Сценарий проверки получения курса по идентификатору.

    Проверяет корректность передачи параметра пути через все слои приложения
    и правильность сериализации ответа.
    """

    response = await client.get(f'/api/courses/{seeded_course_tree.course_id}')

    assert response.status_code == 200
    payload = response.json()
    assert payload['id'] == seeded_course_tree.course_id
    assert payload['title'] == seeded_course_tree.course_title


async def test_get_course_returns_404_when_course_is_missing(client: AsyncClient) -> None:
    """
    Сценарий проверки обработки отсутствующего курса.

    Проверяет полный путь обработки ошибки: от выброса исключения в use case
    до возврата корректного статус-кода 404 с ожидаемым форматом ошибки.
    """

    response = await client.get(f'/api/courses/{uuid4()}')

    assert response.status_code == 404
    payload = response.json()
    assert payload['error'] == 'course_not_found'


async def test_get_course_structure_returns_modules_sections_and_lectures(
    client: AsyncClient, seeded_course_tree: SimpleNamespace
) -> None:
    """
    Сценарий проверки получения полной структуры курса.

    Проверяет, что эндпоинт возвращает вложенное дерево контента
    с курсом, модулями, секциями и лекциями в правильном порядке.
    """

    response = await client.get(f'/api/courses/{seeded_course_tree.course_id}/structure')

    assert response.status_code == 200
    payload = response.json()
    assert payload['title'] == seeded_course_tree.course_title
    assert len(payload['modules']) == 1
    assert len(payload['modules'][0]['sections']) == 1
    assert len(payload['modules'][0]['sections'][0]['lectures']) == 1


async def test_get_lecture_returns_full_content(
    client: AsyncClient, seeded_course_tree: SimpleNamespace
) -> None:
    """
    Сценарий чтения полной лекции по идентификатору.

    Проверяет, что эндпоинт возвращает полный текст лекции,
    а не сокращённую структуру навигации.
    """

    response = await client.get(f'/api/lectures/{seeded_course_tree.lecture_id}')

    assert response.status_code == 200
    payload = response.json()
    assert payload['id'] == seeded_course_tree.lecture_id
    assert payload['content'] == seeded_course_tree.lecture_content
