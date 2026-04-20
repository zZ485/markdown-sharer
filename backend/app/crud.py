from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_
import uuid
from .models import Document


def get_documents(db: Session):
    return db.query(Document).order_by(Document.updated_at.desc()).all()


def get_document(db: Session, document_id: str):
    return db.query(Document).filter(Document.id == document_id).first()


def get_document_by_share_token(db: Session, share_token: str):
    return db.query(Document).filter(Document.share_token == share_token).first()


def create_document(db: Session, title: str, content: str = ""):
    doc = Document(title=title, content=content)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def update_document(db: Session, doc: Document, title: str = None, content: str = None):
    if title is not None:
        doc.title = title
    if content is not None:
        doc.content = content
    db.commit()
    db.refresh(doc)
    return doc


def delete_document(db: Session, doc: Document):
    db.delete(doc)
    db.commit()


def create_share_token(db: Session, doc: Document):
    share_token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=7)
    doc.share_token = share_token
    doc.expires_at = expires_at
    db.commit()
    db.refresh(doc)
    return share_token, expires_at


def is_share_valid(doc: Document):
    if not doc.share_token or not doc.expires_at:
        return False
    return datetime.utcnow() < doc.expires_at
