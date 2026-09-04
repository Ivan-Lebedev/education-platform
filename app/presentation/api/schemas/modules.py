from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ModuleWriteRequest(BaseModel):
    "Базовая схема данных тела запроса при взаимодействии с модулем курса."

    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    position: int = Field(ge=1)


class CreateModuleRequest(ModuleWriteRequest):
    "Схема данных тела запроса при создании модуля курса."


class UpdateModuleRequest(ModuleWriteRequest):
    "Схема данных тела запроса при обновлении модуля курса."


class ModuleResponse(BaseModel):
    "Схема данных тела ответа при получении модуля курса."

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    course_id: UUID
    title: str
    description: str
    position: int
