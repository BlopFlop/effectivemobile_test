from datetime import date
from typing import Any, Optional

from pydantic import BaseModel, Field


class BookSchema(BaseModel):
    """Pydantic schema for Book."""

    id: int = Field(
        title="Уникальный айди Книги в json",
    )
    title: str = Field(
        title="Название книги",
    )
    author: str = Field(
        title="Автор",
    )
    year: int = Field(
        title="Год издания",
    )
    availability: bool = Field(
        title="Наличие книги",
    )

    class Config:
        json_schema_extra: dict[str, Any] = {
            "example": {
                "id": 1,
                "title": "Основы Python",
                "author": "Лутц",
                "year": 2023,
                "availability": True
            }
        }

    def __str__(self) -> str:
        return f"Book {self.title}"


class BookSchemaUpdate(BaseModel):
    """Pydantic schema for Book."""

    id: int = Field(
        title="Уникальный айди Книги в json",
    )
    title: str = Field(
        title="Название книги",
    )
    author: str = Field(
        title="Автор",
    )
    year: int = Field(
        title="Год издания",
    )
    availability: bool = Field(
        title="Наличие книги",
    )

    def __str__(self) -> str:
        return f"Book {self.title}"
