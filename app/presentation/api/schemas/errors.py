from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Единый внешний JSON-контракт ошибки."""

    error: str
    message: str
