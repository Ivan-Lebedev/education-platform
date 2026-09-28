from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domain.entities.user import UserRole


class RegisterUserRequest(BaseModel):
    "Схема данных тела запроса при создании (регистрации) пользователя."

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class RegisteredUserResponse(BaseModel):
    "Схема данных тела ответа при создании (регистрации) пользователя."

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    role: UserRole


class LoginRequest(BaseModel):
    "Схема данных тела запроса при логине."

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    "Схема данных тела ответа при получении JWT."

    access_token: str
    token_type: str
