from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CourseBaseResponse(BaseModel):
    "Базовая схема данных тела ответа при получении курса."

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str


class CourseListItemResponse(CourseBaseResponse):
    "Схема данных тела ответа при получении списка курсов."


class CourseResponse(CourseBaseResponse):
    "Схема данных тела ответа при получении курса."


class LectureBaseResponse(BaseModel):
    "Базовая схема данных тела ответа при получении лекции."

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    position: int


class LectureResponse(LectureBaseResponse):
    "Схема данных тела ответа при получении лекции."

    content: str
    section_id: UUID


class LectureStructureResponse(LectureBaseResponse):
    "Схема данных тела ответа при получении структуры лекции."


class SectionBaseResponse(BaseModel):
    "Базовая схема данных тела ответа при получении раздела."

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    position: int


class SectionStructureResponse(SectionBaseResponse):
    "Схема данных тела ответа при получении структуры раздела."

    lectures: list[LectureStructureResponse]


class ModuleBaseResponse(BaseModel):
    "Базовая схема данных тела ответа при получении модуля."

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    position: int


class ModuleStructureResponse(ModuleBaseResponse):
    "Схема данных тела ответа при получении структуры модуля."

    sections: list[SectionStructureResponse]


class CourseStructureResponse(CourseBaseResponse):
    "Схема данных тела ответа при получении полной структуры курса."

    modules: list[ModuleStructureResponse]
