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


class InvalidQuestionError(DomainError):
    "Общее исключение сущности 'Вопрос'."


class InvalidAnswerOptionError(DomainError):
    "Общее исключение сущности 'Вариант ответа на вопрос'."


class InvalidQuestionAttemptError(DomainError):
    "Общее исключение сущности 'Попытка ответа на вопрос'."


class QuestionAttemptLimitExceededError(DomainError):
    "Исключение, возникающее когда у студента не осталось попыток ответа на текущий вопрос."


class InvalidQuestionResultError(DomainError):
    "Исключение, возникающее когда ответ на вопрос содержит некорректные данные."


class QuestionAlreadySolvedError(DomainError):
    """
    Исключение, возникающее когда пользователь пытается ответить на вопрос,
    при наличии положительной попытки, сделанной ранее.
    """
