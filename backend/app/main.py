from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from typing import List
from urllib.parse import quote
import os

from .database import engine, Base, get_db
from .models import Document
from .schemas import (
    DocumentCreate,
    DocumentUpdate,
    DocumentResponse,
    DocumentListItem,
    ShareResponse,
)
from .crud import (
    get_documents,
    get_document,
    get_document_by_share_token,
    create_document,
    update_document,
    delete_document,
    create_share_token,
    is_share_valid,
)

os.makedirs("data", exist_ok=True)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Markdown Sharer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def doc_to_response(doc: Document) -> DocumentResponse:
    return DocumentResponse(
        id=doc.id,
        title=doc.title,
        content=doc.content,
        share_token=doc.share_token,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
        expires_at=doc.expires_at,
    )


def doc_to_list_item(doc: Document) -> DocumentListItem:
    return DocumentListItem(
        id=doc.id,
        title=doc.title,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
        has_share_link=doc.share_token is not None,
    )


@app.post("/api/documents", response_model=DocumentResponse)
def api_create_document(
    data: DocumentCreate, db: Session = Depends(get_db)
):
    doc = create_document(db, data.title, data.content)
    return doc_to_response(doc)


@app.get("/api/documents", response_model=List[DocumentListItem])
def api_list_documents(db: Session = Depends(get_db)):
    docs = get_documents(db)
    return [doc_to_list_item(d) for d in docs]


@app.get("/api/documents/{document_id}", response_model=DocumentResponse)
def api_get_document(document_id: str, db: Session = Depends(get_db)):
    doc = get_document(db, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc_to_response(doc)


@app.put("/api/documents/{document_id}", response_model=DocumentResponse)
def api_update_document(
    document_id: str, data: DocumentUpdate, db: Session = Depends(get_db)
):
    doc = get_document(db, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    doc = update_document(db, doc, data.title, data.content)
    return doc_to_response(doc)


@app.delete("/api/documents/{document_id}")
def api_delete_document(document_id: str, db: Session = Depends(get_db)):
    doc = get_document(db, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    delete_document(db, doc)
    return {"message": "Document deleted"}


@app.post("/api/documents/{document_id}/share", response_model=ShareResponse)
def api_create_share(document_id: str, db: Session = Depends(get_db)):
    doc = get_document(db, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    share_token, expires_at = create_share_token(db, doc)
    return ShareResponse(share_url=f"/share/{share_token}", expires_at=expires_at)


@app.get("/api/share/{token}", response_model=DocumentResponse)
def api_view_shared(token: str, db: Session = Depends(get_db)):
    doc = get_document_by_share_token(db, token)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if not is_share_valid(doc):
        raise HTTPException(status_code=410, detail="Share link has expired")
    return doc_to_response(doc)


@app.get("/api/share/{token}/download")
def api_download_shared(token: str, db: Session = Depends(get_db)):
    doc = get_document_by_share_token(db, token)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if not is_share_valid(doc):
        raise HTTPException(status_code=410, detail="Share link has expired")
    filename = f"{doc.title}.md"
    encoded_filename = quote(filename)
    return PlainTextResponse(
        content=doc.content,
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"},
    )
