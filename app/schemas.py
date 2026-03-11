"""Pydantic schemas for request/response."""
from datetime import datetime
from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    """Base todo schema."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(default="", max_length=1024)
    completed: bool = False


class TodoCreate(TodoBase):
    """Schema for creating a todo."""

    pass


class TodoUpdate(BaseModel):
    """Schema for updating a todo (all fields optional)."""

    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1024)
    completed: bool | None = None


class TodoResponse(TodoBase):
    """Schema for todo response."""

    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
