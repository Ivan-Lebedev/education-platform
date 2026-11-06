from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

from app.domain.exceptions import InvalidUserError


class UserRole(StrEnum):
    "Варианты значений поля role сущности 'Пользователь'."

    STUDENT = 'student'
    AUTHOR = 'author'
    ADMIN = 'admin'


@dataclass(slots=True)
class User:
    "Доменная сущность 'Пользователь'."

    id: UUID
    email: str
    hashed_password: str
    role: UserRole

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.email or '@' not in self.email:
            raise InvalidUserError('User email is invalid.')
        if not self.hashed_password or not self.hashed_password.strip():
            raise InvalidUserError('User hashed password cannot be empty.')

    def is_admin(self) -> bool:
        return self.role is UserRole.ADMIN

    def is_author(self) -> bool:
        return self.role is UserRole.AUTHOR

    def is_student(self) -> bool:
        return self.role is UserRole.STUDENT

    def can_manage_platform(self) -> bool:
        "Возможность администрирования платформы."

        return self.is_admin()

    def can_manage_learning_content(self) -> bool:
        "Возможность работать с курсами, разделами, лекциями и другими учебными элементами."

        return self.role in {UserRole.ADMIN, UserRole.AUTHOR}

    def can_manage_course_structure(self) -> bool:
        "Возможность работать не с отдельными фрагментами, а со структурой курса целиком."

        return self.role in {UserRole.ADMIN, UserRole.AUTHOR}

    def can_manage_interactive_content(self) -> bool:
        "Возможность работать с интерактивной частью контента курса."

        return self.role in {UserRole.ADMIN, UserRole.AUTHOR}

    def can_take_learning_activities(self) -> bool:
        "Возможность участия в учебных активностях."

        return self.is_student()

    def can_view_own_learning_results(self) -> bool:
        "Возможность просмотра собственных результатов учебы."

        return self.is_student()

    def can_view_all_learning_results(self) -> bool:
        "Возможность просмотра результатов учебы всех студентов."

        return self.role in {UserRole.ADMIN, UserRole.AUTHOR}

    def can_manage_content(self) -> bool:
        return self.can_manage_learning_content()
