from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator

class DocumentCreate(BaseModel):
    title: str
    content: str

    @field_validator("title", "content")
    @classmethod
    def must_not_be_blank(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be empty")
        return value

class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DocumentSearchResult(BaseModel):
    id: int
    title: str
    content: str
    score: float

    model_config = ConfigDict(from_attributes=True)