class ApplicationError(Exception):
    """Базовое исключение слоя приложения."""


class CourseNotFoundError(ApplicationError):
    "Исключение, возникающее при отсутствии запрашиваемого курса."


class LectureNotFoundError(ApplicationError):
    "Исключение, возникающее при отсутствии запрашиваемой лекции."


class ModuleNotFoundError(ApplicationError):
    "Исключение, возникающее при отсутствии запрашиваемого модуля."


class SectionNotFoundError(ApplicationError):
    "Исключение, возникающее при отсутствии запрашиваемого раздела."
