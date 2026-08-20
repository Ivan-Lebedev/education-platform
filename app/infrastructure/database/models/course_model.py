from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class CourseModel(Base):
    """
    SQLAlchemy-модель сущности 'Курс'.

    Атрибуты — название (тип): Описание:
        id (str): УИН экземпляра;
        title (str): Название курса;
        description (str): Описание курса.
    """

    __tablename__ = 'courses'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String)

    modules = relationship(
        'ModuleModel',
        back_populates='course',
        cascade='all, delete-orphan',
        order_by='ModuleModel.position',
    )
