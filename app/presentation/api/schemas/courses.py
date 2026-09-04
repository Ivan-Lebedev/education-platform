from pydantic import BaseModel, Field


class CourseWriteRequest(BaseModel):
    "Базовая схема данных тела запроса при взаимодействии с курсом."

    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)


class CreateCourseRequest(CourseWriteRequest):
    "Схема данных тела запроса при создании курса."


class UpdateCourseRequest(CourseWriteRequest):
    "Схема данных тела запроса при обновлении курса."
