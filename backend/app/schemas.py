from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class DocumentCreate(BaseModel):
    title: str
    content: str = ""


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class DocumentResponse(BaseModel):
    id: str
    title: str
    content: str
    share_token: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DocumentListItem(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    has_share_link: bool

    class Config:
        from_attributes = True


class ShareResponse(BaseModel):
    share_url: str
    expires_at: datetime
