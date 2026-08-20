from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class LectureModel(Base):
    """
    SQLAlchemy-модель сущности 'Лекция'.

    Атрибуты — название (тип): Описание:
        id (str): УИН экземпляра;
        section_id (str): УИН экземпляра раздела, в который входит лекция;
        title (str): Название лекции;
        content (str): Содержание лекции;
        position (int): Позиционный номер лекции в составе раздела.

    Связи — название (Модель): Описание:
        section (SectionModel): Раздел, в которой входит лекция (N:1).
    """

    __tablename__ = 'lectures'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    section_id: Mapped[str] = mapped_column(ForeignKey('sections.id', ondelete='CASCADE'))
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    position: Mapped[int] = mapped_column(Integer)

    section = relationship('SectionModel', back_populates='lectures')
