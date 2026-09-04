from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SectionWriteRequest(BaseModel):
    "Базовая схема данных тела запроса при взаимодействии с разделом модуля курса."

    title: str = Field(min_length=1, max_length=255)
    description: str = ''
    position: int = Field(ge=1)


class CreateSectionRequest(SectionWriteRequest):
    "Схема данных тела запроса при создании раздела модуля курса."


class UpdateSectionRequest(SectionWriteRequest):
    "Схема данных тела запроса при обновлении раздела модуля курса."


class SectionResponse(BaseModel):
    "Схема данных тела ответа при получении раздела модуля курса."

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    module_id: UUID
    title: str
    description: str
    position: int
