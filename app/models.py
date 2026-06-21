from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone
from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    embedding = Column(Text, nullable=False)