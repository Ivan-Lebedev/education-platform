from types import SimpleNamespace
from uuid import uuid4

from httpx import AsyncClient


async def test_get_courses_returns_public_list(
    client: AsyncClient, seeded_course_tree: SimpleNamespace
) -> None:
    """
    Сценарий получения списка курсов.

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
    Сценарий получения курса по идентификатору.

    Проверяет, что маршрут возвращает статус-код 200 и корректные данные курса
    (идентификатор и название) для существующего курса.
    """

    response = await client.get(f'/api/courses/{seeded_course_tree.course_id}')

    assert response.status_code == 200
    payload = response.json()
    assert payload['id'] == seeded_course_tree.course_id
    assert payload['title'] == seeded_course_tree.course_title


async def test_get_course_returns_404_when_course_is_missing(client: AsyncClient) -> None:
    """
    Сценарий запроса несуществующего курса.

    Проверяет, что маршрут возвращает статус-код 404 с ожидаемым форматом ошибки
    при запросе курса с несуществующим идентификатором.
    """

    response = await client.get(f'/api/courses/{uuid4()}')

    assert response.status_code == 404
    payload = response.json()
    assert payload['error'] == 'course_not_found'


async def test_get_course_structure_returns_modules_sections_and_lectures(
    client: AsyncClient, seeded_course_tree: SimpleNamespace
) -> None:
    """
    Сценарий получения полной структуры курса.

    Проверяет, что маршрут возвращает статус-код 200 и вложенное дерево контента
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
    Сценарий получения полной лекции по идентификатору.

    Проверяет, что маршрут возвращает статус-код 200 и полный текст лекции,
    а не сокращённую структуру навигации.
    """

    response = await client.get(f'/api/lectures/{seeded_course_tree.lecture_id}')

    assert response.status_code == 200
    payload = response.json()
    assert payload['id'] == seeded_course_tree.lecture_id
    assert payload['content'] == seeded_course_tree.lecture_content


async def test_delete_lecture(
    client: AsyncClient,
    seeded_course_tree: SimpleNamespace,
    admin_auth_headers: dict[str, str],
) -> None:
    "Сценарий удаления лекции по идентификатору."

    delete_response = await client.delete(
        f'/api/admin/lectures/{seeded_course_tree.lecture_id}',
        headers=admin_auth_headers,
    )
    assert delete_response.status_code == 204

    lecture_response = await client.get(f'/api/lectures/{seeded_course_tree.lecture_id}')
    assert lecture_response.status_code == 404
    lecture_response_payload = lecture_response.json()
    assert lecture_response_payload['error'] == 'lecture_not_found'
    assert lecture_response_payload['message'] == 'Lecture not found.'

    course_structure_response = await client.get(
        f'/api/courses/{seeded_course_tree.course_id}/structure'
    )
    assert course_structure_response.status_code == 200
    course_structure_response_payload = course_structure_response.json()
    assert course_structure_response_payload['title'] == seeded_course_tree.course_title
    assert len(course_structure_response_payload['modules']) == 1
    assert len(course_structure_response_payload['modules'][0]['sections']) == 1
    assert len(course_structure_response_payload['modules'][0]['sections'][0]['lectures']) == 0


async def test_delete_section(
    client: AsyncClient,
    seeded_course_tree: SimpleNamespace,
    admin_auth_headers: dict[str, str],
) -> None:
    "Сценарий удаления раздела по идентификатору."

    delete_response = await client.delete(
        f'/api/admin/sections/{seeded_course_tree.section_id}',
        headers=admin_auth_headers,
    )
    assert delete_response.status_code == 204

    course_structure_response = await client.get(
        f'/api/courses/{seeded_course_tree.course_id}/structure'
    )
    assert course_structure_response.status_code == 200
    course_structure_response_payload = course_structure_response.json()
    assert course_structure_response_payload['title'] == seeded_course_tree.course_title
    assert len(course_structure_response_payload['modules']) == 1
    assert len(course_structure_response_payload['modules'][0]['sections']) == 0


async def test_delete_module(
    client: AsyncClient,
    seeded_course_tree: SimpleNamespace,
    admin_auth_headers: dict[str, str],
) -> None:
    "Сценарий удаления модуля по идентификатору."

    delete_response = await client.delete(
        f'/api/admin/modules/{seeded_course_tree.module_id}',
        headers=admin_auth_headers,
    )
    assert delete_response.status_code == 204

    course_structure_response = await client.get(
        f'/api/courses/{seeded_course_tree.course_id}/structure'
    )
    assert course_structure_response.status_code == 200
    course_structure_response_payload = course_structure_response.json()
    assert course_structure_response_payload['title'] == seeded_course_tree.course_title
    assert len(course_structure_response_payload['modules']) == 0


async def test_delete_course(
    client: AsyncClient,
    seeded_course_tree: SimpleNamespace,
    admin_auth_headers: dict[str, str],
) -> None:
    "Сценарий удаления курса по идентификатору."

    delete_response = await client.delete(
        f'/api/admin/courses/{seeded_course_tree.module_id}',
        headers=admin_auth_headers,
    )
    assert delete_response.status_code == 204

    course_structure_response = await client.get(
        f'/api/courses/{seeded_course_tree.course_id}/structure'
    )
    assert course_structure_response.status_code == 404
    course_structure_response_payload = course_structure_response.json()
    assert course_structure_response_payload['error'] == 'course_not_found'
    assert course_structure_response_payload['message'] == 'Course not found.'
