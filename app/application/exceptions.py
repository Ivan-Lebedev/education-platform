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


class UserAlreadyExistsError(ApplicationError):
    """
    Исключение, возникающее при попытке создания пользователя
    с учетными данными, уже имеющимися в БД.
    """


class InvalidCredentialsError(ApplicationError):
    "Исключение, возникающее при предоставлении неверных учетных данных."


class QuestionNotFoundError(ApplicationError):
    "Исключение, возникающее при отсутствии запрашиваемого вопроса."


class PermissionDeniedError(ApplicationError):
    "Исключение, возникающее при недостатке прав пользователя."


class AnswerOptionNotFoundError(ApplicationError):
    "Исключение, возникающее при отсутствии запрашиваемого варианта ответа на вопрос."


class QuestionAlreadyUsedError(ApplicationError):
    "Исключение, возникающее при попытке изменить вопрос, уже вошедший в реальный учебный процесс."
