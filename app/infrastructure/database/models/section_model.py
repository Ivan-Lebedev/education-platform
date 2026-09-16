from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class SectionModel(Base):
    """
    SQLAlchemy-модель сущности 'Раздел'.

    Attributes:
        id (str): УИН экземпляра.
        module_id (str): УИН экземпляра модуля, в который входит раздел.
        title (str): Название раздела.
        description (str): Описание раздела.
        position (int): Позиционный номер раздела в составе модуля.

        module (ModuleModel): Связь N:1. Модуль, в который входит раздел.
        lectures (List[LectureModel]): Связь 1:N. Лекции, которые входят в раздел.
    """

    __tablename__ = 'sections'

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    module_id: Mapped[str] = mapped_column(ForeignKey('modules.id', ondelete='CASCADE'))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String, default='')
    position: Mapped[int] = mapped_column(Integer)

    module = relationship('ModuleModel', back_populates='sections')
    lectures = relationship(
        'LectureModel',
        back_populates='section',
        cascade='all, delete-orphan',
        order_by='LectureModel.position',
    )
