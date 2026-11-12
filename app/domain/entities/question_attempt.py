from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID

from app.domain.exceptions import InvalidQuestionAttemptError


class QuestionResultStatus(StrEnum):
    "Варианты значений поля 'result_status' сущности 'Попытка ответа на вопрос'."

    CORRECT = 'correct'
    INCORRECT = 'incorrect'


@dataclass(slots=True)
class QuestionAttempt:
    """
    Доменная сущность 'Попытка ответа на вопрос'.

    Attributes:
        id (UUID): УИН экземпляра сущности.
        question_id (UUID): УИН вопроса, которому принадлежит попытка.
        student_id (UUID): УИН студента, которому принадлежит попытка.
        attempt_number (int): Порядковый номер попытки.
        selected_option_ids list[UUID]: УИН выбранных студентом вариантов ответов на вопрос.
        created_at (datetime): Дата и время попытки ответа на вопрос.
        result_status (QuestionResultStatus | None): Статус попытки.
        awarded_points (int | None): Начисленные баллы за попытку.
        checked_at (datetime | None): Дата и время проверки попытки.
    """

    id: UUID
    question_id: UUID
    student_id: UUID
    attempt_number: int
    selected_option_ids: list[UUID] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    result_status: QuestionResultStatus | None = None
    awarded_points: int | None = None
    checked_at: datetime | None = None

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

    def is_first_attempt(self) -> bool:
        return self.attempt_number == 1

    def is_repeat_attempt(self) -> bool:
        return self.attempt_number > 1

    def has_selected_options(self) -> bool:
        return bool(self.selected_option_ids)

    def selected_options_count(self) -> int:
        return len(self.selected_option_ids)

    def uses_option(self, answer_option_id: UUID) -> bool:
        return answer_option_id in self.selected_option_ids

    def has_result(self) -> bool:
        return self.result_status is not None

    def is_correct(self) -> bool:
        return self.result_status is QuestionResultStatus.CORRECT

    def is_incorrect(self) -> bool:
        return self.result_status is QuestionResultStatus.INCORRECT

    def apply_result(
        self,
        result_status: QuestionResultStatus,
        awarded_points: int,
    ) -> None:
        """
        Валидация и фиксация попытки ответа на вопрос, путем перевода ее из состояния
        «есть зафиксированный ответ» в состояние «есть проверенный и завершенный ответ».

        Правила валидации:
            - Нельзя повторно назначать результат уже проверенной попытке.
            - Нельзя начислять отрицательные баллы за попытку.
            - Неправильная попытка не может принести баллы.
        Raises:
            InvalidQuestionAttemptError: Если нарушено хотя бы одно правило валидации.
        """

        if self.has_result():
            raise InvalidQuestionAttemptError('Question attempt result is already defined.')
        if awarded_points < 0:
            raise InvalidQuestionAttemptError('Awarded points cannot be negative.')
        if result_status is QuestionResultStatus.INCORRECT and awarded_points != 0:
            raise InvalidQuestionAttemptError(
                'Incorrect question attempt cannot have awarded points.'
            )

        self.result_status = result_status
        self.awarded_points = awarded_points
        self.checked_at = datetime.now(UTC)
