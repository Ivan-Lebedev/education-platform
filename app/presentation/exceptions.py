class PresentationError(Exception):
    """Базовое исключение слоя представления."""


class AuthenticationError(PresentationError):
    "Исключение, возникающее при ошибке аутентификации пользователя."


class PermissionDeniedError(PresentationError):
    "Исключение, возникающее при ошибке проверки прав пользователя."
