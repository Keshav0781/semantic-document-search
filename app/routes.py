from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Document
from app.schemas import DocumentCreate, DocumentResponse, DocumentSearchResult
from app.embeddings import compute_embedding, cosine_similarity
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

@router.get("/documents/search", response_model=list[DocumentSearchResult])
def search_documents(q: str, top_k: int = 5, filter_title: str = None, db: Session = Depends(get_db)):
    query_embedding = compute_embedding(q)

    if filter_title is not None:
        all_documents = db.query(Document).filter(Document.title.contains(filter_title)).all()
    else:
        all_documents = db.query(Document).all()

    results = []
    for doc in all_documents:
        doc_embedding = json.loads(doc.embedding)
        score = cosine_similarity(query_embedding, doc_embedding)
        results.append(
            {
                "id": doc.id,
                "title": doc.title,
                "content": doc.content,
                "score": score,
            }
        )

    results.sort(key=lambda r: r["score"], reverse=True)

    return results[:top_k]



@router.delete("/documents/{id}")
def delete_document(id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == id).first()

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    db.delete(document)
    db.commit()

    return {"detail": "Document deleted successfully"}