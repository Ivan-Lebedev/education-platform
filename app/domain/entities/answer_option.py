from dataclasses import dataclass
from uuid import UUID

from app.domain.exceptions import InvalidAnswerOptionError


@dataclass(slots=True)
class AnswerOption:
    """
    Доменная сущность 'Вариант ответа на вопрос' — блок внутри сущности 'Вопрос'.

    Attributes:
        id (UUID): УИН экземпляра сущности.
        question_id (UUID): Вопрос, к которому принадлежит вариант ответа на вопрос.
        text (str): Содержимое варианта ответа на вопрос.
        position (int): Порядковый номер варианта ответа на вопрос внутри вопроса.
        is_correct (bool): Является ли данный вариант ответа на вопрос верным.
    """

    id: UUID
    question_id: UUID
    text: str
    position: int
    is_correct: bool = False

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.text or not self.text.strip():
            raise InvalidAnswerOptionError('Answer option text cannot be empty.')
        if self.position < 1:
            raise InvalidAnswerOptionError('Answer option position must be positive.')

    def update(self, text: str, position: int, is_correct: bool) -> None:
        self.text = text
        self.position = position
        self.is_correct = is_correct
        self._validate()
