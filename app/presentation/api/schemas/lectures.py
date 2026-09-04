from pydantic import BaseModel, Field


class LectureWriteRequest(BaseModel):
    "Базовая схема данных тела запроса при взаимодействии с лекцией из раздела модуля курса."

    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
    position: int = Field(ge=1)


class CreateLectureRequest(LectureWriteRequest):
    "Схема данных тела запроса при создании лекции из раздела модуля курса."


class UpdateLectureRequest(LectureWriteRequest):
    "Схема данных тела запроса при создании лекции из раздела модуля курса."
