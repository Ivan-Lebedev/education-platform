from httpx import AsyncClient

from app.infrastructure.database.models.user_model import UserModel


async def test_register_creates_student_user(client: AsyncClient) -> None:
    """
    Сценарий успешной регистрации пользователя.

    Проверяет, что маршрут возвращает статус-код 201 и ожидаемые данные пользователя.
    """

    response = await client.post(
        '/api/auth/register',
        json={
            'email': 'student@example.com',
            'password': 'strongpassword123',
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload['email'] == 'student@example.com'
    assert payload['role'] == 'student'


async def test_register_returns_400_when_user_already_exists(
    client: AsyncClient, seeded_student_user: UserModel
) -> None:
    """
    Сценарий регистрации при наличии пользователя с указанным email.

    Проверяет, что маршрут возвращает статус-код 400 с ожидаемой ошибкой
    при попытке создать пользователя с уже существующим email.
    """

    response = await client.post(
        '/api/auth/register',
        json={
            'email': 'student@example.com',
            'password': 'anotherpassword123',
        },
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload['error'] == 'application_error'


async def test_login_returns_access_token(
    client: AsyncClient, seeded_student_user: UserModel
) -> None:
    """
    Сценарий успешного входа в систему пользователя.

    Проверяет, что маршрут возвращает статус-код 200 и ожидаемый токен пользователя.
    """

    response = await client.post(
        '/api/auth/login',
        json={
            'email': 'student@example.com',
            'password': 'strongpassword123',
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload['token_type'] == 'bearer'
    assert 'access_token' in payload


async def test_login_returns_400_for_invalid_credentials(client: AsyncClient) -> None:
    """
    Сценарий входа с недействительными учётными данными.

    Проверяет, что маршрут возвращает статус-код 400 с ожидаемой ошибкой
    при попытке войти с несуществующим email или неверным паролем.
    """

    response = await client.post(
        '/api/auth/login',
        json={
            'email': 'missing@example.com',
            'password': 'wrongpassword',
        },
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload['error'] == 'application_error'


async def test_auth_me_returns_current_user(
    client: AsyncClient,
    student_auth_headers: dict[str, str],
) -> None:
    """
    Сценарий получения данных текущего аутентифицированного пользователя.

    Проверяет, что маршрут с валидным токеном возвращает статус-код 200
    и корректные данные пользователя (email, role).
    """

    response = await client.get('/api/auth/me', headers=student_auth_headers)

    assert response.status_code == 200
    payload = response.json()
    assert payload['email'] == 'student@example.com'
    assert payload['role'] == 'student'


async def test_admin_route_returns_401_without_token(client: AsyncClient):
    """
    Сценарий доступа к административному маршруту без токена.

    Проверяет, что маршрут возвращает статус-код 401 с ожидаемой ошибкой
    при запросе без заголовка Authorization.
    """

    response = await client.post(
        '/api/admin/courses',
        json={
            'title': 'New course',
            'description': 'Description',
        },
    )

    assert response.status_code == 401
    payload = response.json()
    assert payload['error'] == 'authentication_error'


async def test_admin_route_returns_403_for_student(
    client: AsyncClient,
    student_auth_headers: dict[str, str],
) -> None:
    """
    Сценарий доступа к административному маршруту пользователя без прав администратора.

    Проверяет, что маршрут возвращает статус-код 403 с ожидаемой ошибкой
    при запросе пользователя, не имеющего роли admin.
    """

    response = await client.post(
        '/api/admin/courses',
        headers=student_auth_headers,
        json={
            'title': 'New course',
            'description': 'Description',
        },
    )

    assert response.status_code == 403
    payload = response.json()
    assert payload['error'] == 'permission_denied'


async def test_admin_route_allows_admin_user(
    client: AsyncClient, admin_auth_headers: dict[str, str]
) -> None:
    """
    Сценарий успешного создания курса администратором.

    Проверяет, что административный маршрут возвращает статус-код 201
    при запросе с валидным токеном пользователя с ролью admin.
    """

    response = await client.post(
        '/api/admin/courses',
        headers=admin_auth_headers,
        json={
            'title': 'Admin course',
            'description': 'Created by admin.',
        },
    )

    assert response.status_code == 201
