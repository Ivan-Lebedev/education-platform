from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from app.domain.exceptions import InvalidQuestionAttemptError


@dataclass(slots=True)
class QuestionAttempt:
    """
    Доменная сущность 'Попытка ответа на вопрос'.

    Attributes:
        id (UUID): УИН экземпляра сущности.
        question_id (UUID): Вопрос, которому принадлежит попытка ответа на вопрос.
        student_id (UUID): Студент, которому принадлежит попытка ответа на вопрос.
        attempt_number (int): Порядковый номер попытки ответа на вопрос.
        selected_option_ids list[UUID]: Выбранные варианты ответов на вопрос.
        created_at (datetime): Дата и время попытки ответа на вопрос.
    """

    id: UUID
    question_id: UUID
    student_id: UUID
    attempt_number: int
    selected_option_ids: list[UUID] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if self.attempt_number < 1:
            raise InvalidQuestionAttemptError('Question attempt number must be positive.')
        if not self.selected_option_ids:
            raise InvalidQuestionAttemptError(
                'Question attempt must contain at least one selected option.'
            )
        if len(self.selected_option_ids) != len(set(self.selected_option_ids)):
            raise InvalidQuestionAttemptError(
                'Question attempt cannot contain duplicate selected options.'
            )
