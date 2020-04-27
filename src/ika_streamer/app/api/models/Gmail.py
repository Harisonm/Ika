from pydantic import BaseModel
from typing import List, Optional

class Gmail(BaseModel):
    _id: str
    idMail: Optional[str] = None
    threadId: Optional[str] = None
    historyId: Optional[str] = None
    From: Optional[str] = None
    to: Optional[str] = None
    date: Optional[str] = None
    labelIds: Optional[str] = None
    spam: Optional[str] = None
    body: Optional[str] = None
    mimeType: Optional[str] = None