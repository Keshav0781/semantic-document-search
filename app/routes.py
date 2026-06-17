from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Document
from app.schemas import DocumentCreate, DocumentResponse
from app.embeddings import compute_embedding
import json

router = APIRouter()


@router.post("/documents", response_model=DocumentResponse)
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    embedding = compute_embedding(document.content)

    new_document = Document(
        title=document.title,
        content=document.content,
        embedding=json.dumps(embedding),
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document