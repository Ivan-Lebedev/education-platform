class ApplicationError(Exception):
    """Базовое исключение слоя приложения."""


class CourseNotFoundError(ApplicationError):
    pass


class LectureNotFoundError(ApplicationError):
    pass
