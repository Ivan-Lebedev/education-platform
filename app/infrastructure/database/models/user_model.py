from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.models.base import Base


class UserModel(Base):
    """
    SQLAlchemy-модель сущности 'Пользователь'.

    Атрибуты — название (тип): Описание:
        id (str): УИН экземпляра;
        email (str): Электронная почта пользователя;
        hashed_password (str): Хеш пароля пользователя;
        role (str): Роль пользователя.
    """

    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50))
