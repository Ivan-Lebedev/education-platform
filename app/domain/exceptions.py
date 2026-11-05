class DomainError(Exception):
    """Базовое исключение доменного слоя."""


class InvalidCourseError(DomainError):
    "Общее исключение сущности 'Курс'."


class InvalidModuleError(DomainError):
    "Общее исключение сущности 'Модуль'."


class InvalidSectionError(DomainError):
    "Общее исключение сущности 'Раздел'."


class InvalidLectureError(DomainError):
    "Общее исключение сущности 'Лекция'."


class InvalidUserError(DomainError):
    "Общее исключение сущности 'Пользователь'."


class SectionQuestionAlreadyAttachedError(DomainError):
    """
    Исключение, возникающее если попытаться добавить id вопроса в раздел,
    где этот вопрос уже присутствует.
    """


class SectionQuestionNotAttachedError(DomainError):
    "Исключение, возникающее когда запрашиваемый вопрос отсутствует в разделе."
