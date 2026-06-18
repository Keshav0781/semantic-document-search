from datetime import datetime
from pydantic import BaseModel, ConfigDict

class DocumentCreate(BaseModel):
    title: str
    content: str


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