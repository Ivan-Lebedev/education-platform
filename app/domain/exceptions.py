class DomainError(Exception):
    """Базовое исключение доменного слоя."""


class InvalidCourseError(DomainError):
    pass


class InvalidModuleError(DomainError):
    pass


class InvalidSectionError(DomainError):
    pass


class InvalidLectureError(DomainError):
    pass


class InvalidUserError(DomainError):
    pass
