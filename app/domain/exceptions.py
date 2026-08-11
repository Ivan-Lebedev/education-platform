class DomainError(Exception):
    """Базовое исключение доменного слоя."""


class InvalidCourseError(DomainError):
    pass


class InvalidModuleError(DomainError):
    pass
