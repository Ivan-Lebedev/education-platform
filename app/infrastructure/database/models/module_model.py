from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class ModuleModel(Base):
    """
    SQLAlchemy-модель сущности 'Модуль'.

    Attributes:
        id (str): УИН экземпляра.
        course_id (str): УИН экземпляра курса, в который входит модуль.
        title (str): Название модуля.
        description (str): Описание модуля.
        position (int): Позиционный номер модуля в составе курса.

        course (CourseModel): Связь N:1. Курс, в который входит модуль.
        sections (List[SectionModel]): Связь 1:N. Разделы, которые входят в модуль.
    """

    __tablename__ = 'modules'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    course_id: Mapped[str] = mapped_column(ForeignKey('courses.id', ondelete='CASCADE'))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String)
    position: Mapped[int] = mapped_column(Integer)

    course = relationship('CourseModel', back_populates='modules')
    sections = relationship(
        'SectionModel',
        back_populates='module',
        cascade='all, delete-orphan',
        order_by='SectionModel.position',
    )
