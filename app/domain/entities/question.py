from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID

from app.domain.exceptions import (
    InvalidQuestionError,
    QuestionAttemptLimitExceededError,
)


class QuestionType(StrEnum):
    """
    "Варианты значений поля question_type сущности 'Вопрос'."

    Attributes:
        SINGLE_CHOICE (str): Студент должен выбрать ровно один вариант.
        MULTIPLE_CHOICE (str): Студент может и должен выбрать несколько вариантов.
    """

    SINGLE_CHOICE = 'single_choice'
    MULTIPLE_CHOICE = 'multiple_choice'


@dataclass(slots=True)
class Question:
    """
    Доменная сущность 'Вопрос' — блок внутри сущности 'Раздел'.

    Attributes:
        id (UUID): УИН экземпляра сущности.
        section_id (UUID): Раздел, к которому принадлежит вопрос.
        text (str): Формулировка вопроса.
        position (int): Порядковый номер вопроса внутри раздела.
        question_type (QuestionType): Тип вопроса.
        answer_option_ids list[UUID]: Варианты ответа на вопрос.
        max_attempts (int): Количество разрешенных попыток ответа.
        reward_points (int): Количество учебных баллов, получаемых студентом за верный ответ.
    """

    id: UUID
    section_id: UUID
    text: str
    position: int
    question_type: QuestionType = QuestionType.SINGLE_CHOICE
    answer_option_ids: list[UUID] = field(default_factory=list[UUID])
    max_attempts: int = 1
    reward_points: int = 1

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.text or not self.text.strip():
            raise InvalidQuestionError('Question text cannot be empty.')
        if self.position < 1:
            raise InvalidQuestionError('Question position must be positive.')
        if self.max_attempts < 1:
            raise InvalidQuestionError('Question max_attempts must be positive.')
        if self.reward_points < 1:
            raise InvalidQuestionError('Question reward_points must be positive.')

    def update(
        self,
        text: str,
        position: int,
        question_type: QuestionType,
        max_attempts: int,
        reward_points: int,
    ) -> None:
        self.text = text
        self.position = position
        self.question_type = question_type
        self.max_attempts = max_attempts
        self.reward_points = reward_points
        self._validate()

    def add_answer_option(self, answer_option_id: UUID) -> None:
        if answer_option_id not in self.answer_option_ids:
            self.answer_option_ids.append(answer_option_id)

    def remove_answer_option(self, answer_option_id: UUID) -> None:
        if answer_option_id in self.answer_option_ids:
            self.answer_option_ids.remove(answer_option_id)

    def has_answer_options(self) -> bool:
        return bool(self.answer_option_ids)

    def is_single_choice(self) -> bool:
        "Является ли вопрос одиночным выбором."

        return self.question_type is QuestionType.SINGLE_CHOICE

    def is_multiple_choice(self) -> bool:
        "Является ли вопрос множественным выбором."

        return self.question_type is QuestionType.MULTIPLE_CHOICE

    def allows_multiple_answers(self) -> bool:
        "Можно ли выбрать несколько ответов."

        return self.is_multiple_choice()

    def validate_answer_options_configuration(
        self,
        answer_options: Sequence['AnswerOption'],  # type: ignore  # noqa: F821
    ) -> None:
        """
        Проверяет корректность конфигурации вариантов ответа для вопроса.

        Метод применяет бизнес-правила, зависящие от типа вопроса (одиночный или
        множественный выбор), и выбрасывает исключение при нарушении любого из них.

        Правила валидации:
            1. У вопроса должно быть хотя бы два варианта ответа.
            2. Хотя бы один вариант ответа должен быть правильным.
            3. Для одиночного выбора (SINGLE_CHOICE): правильный вариант ровно один.
            4. Для множественного выбора (MULTIPLE_CHOICE): минимум два правильных варианта.

        Args:
            answer_options (Sequence[AnswerOption]): Список вариантов ответа для проверки.

        Raises:
            InvalidQuestionError: Если нарушено хотя бы одно правило валидации.
        """

        if len(answer_options) < 2:
            raise InvalidQuestionError('Question must have at least two answer options.')

        correct_options_count = sum(1 for option in answer_options if option.is_correct)
        if correct_options_count == 0:
            raise InvalidQuestionError('Question must have at least one correct answer option.')

        if self.is_single_choice() and correct_options_count != 1:
            raise InvalidQuestionError(
                'Single choice question must have exactly one correct answer option.'
            )

        if self.is_multiple_choice() and correct_options_count < 2:
            raise InvalidQuestionError(
                'Multiple choice question must have at least two correct answer options.'
            )

    def can_start_attempt(self, existing_attempts_count: int) -> bool:
        """
        Разрешена ли еще одна попытка при текущем числе уже существующих попыток.

        Args:
            existing_attempts_count (int): Текущее количество реализованных попыток
                ответа на вопрос.
        """

        return existing_attempts_count < self.max_attempts

    def ensure_attempt_available(self, existing_attempts_count: int) -> None:
        """
        Проверяет доступность попыток для ответа на вопрос.

        Args:
            existing_attempts_count (int): Текущее количество реализованных попыток
                ответа на вопрос.

        Raises:
            QuestionAttemptLimitExceededError: Если закончились доступные попытки ответа на вопрос.
        """
        if not self.can_start_attempt(existing_attempts_count):
            raise QuestionAttemptLimitExceededError('Question attempt limit has been reached.')
