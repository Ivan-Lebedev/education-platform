from dataclasses import dataclass, field
from uuid import UUID

from app.domain.exceptions import InvalidQuestionError


@dataclass(slots=True)
class Question:
    """
    Доменная сущность 'Вопрос' — блок внутри сущности 'Раздел'.

    Attributes:
        id (UUID): УИН экземпляра сущности.
        section_id (UUID): Раздел, к которому принадлежит вопрос.
        text (str): Формулировка вопроса.
        position (int): Порядковый номер вопроса внутри раздела.
        answer_option_ids list[UUID]: Варианты ответа на вопрос.
        max_attempts (int): Количество разрешенных попыток ответа.
        reward_points (int): Количество учебных баллов, получаемых студентом за верный ответ.
    """

    id: UUID
    section_id: UUID
    text: str
    position: int
    answer_option_ids: list[UUID] = field(default_factory=list)
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
        max_attempts: int,
        reward_points: int,
    ) -> None:
        self.text = text
        self.position = position
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
