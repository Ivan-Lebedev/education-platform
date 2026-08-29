from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CourseBaseResponse(BaseModel):
    "Базовая схема данных для ответа при запросах курса."

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str


class CourseListItemResponse(CourseBaseResponse):
    "Схема данных для ответа при запросе списка курсов."

    pass


class CourseResponse(CourseBaseResponse):
    "Схема данных для ответа при запросе единичного курса."

    pass


class LectureBaseResponse(BaseModel):
    "Базовая схема данных для ответа при запросах лекции."

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    position: int


class LectureResponse(LectureBaseResponse):
    "Схема данных для ответа при запросе лекции."

    content: str
    section_id: UUID


class LectureStructureResponse(LectureBaseResponse):
    pass


class SectionBaseResponse(BaseModel):
    "Базовая схема данных для ответа при запросах раздела."

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    position: int


class SectionStructureResponse(SectionBaseResponse):
    lectures: list[LectureStructureResponse]


class ModuleBaseResponse(BaseModel):
    "Базовая схема данных для ответа при запросах модуля."

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    position: int


class ModuleStructureResponse(ModuleBaseResponse):
    sections: list[SectionStructureResponse]


class CourseStructureResponse(CourseBaseResponse):
    modules: list[ModuleStructureResponse]
