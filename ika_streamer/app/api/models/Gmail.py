from pydantic import BaseModel
from typing import List, Optional

class GmailIn(BaseModel):
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
    
class GmailOut(BaseModel):
    _id: str
    idMail: Optional[str] = None,
    threadId: Optional[str] = None
    historyId: Optional[str] = None
    labelIds: Optional[str] = None
    snippet: Optional[str] = None
    payloadPartId: Optional[str] = None
    payloadMimeType: Optional[str] = None 
    received: Optional[str] = None
    xGoogleSmtpSource: Optional[str] = None 
    xReceived: Optional[str] = None
    arcMessageSignature: Optional[str] = None
    arcAuthenticationResults: Optional[str] = None
    returnPath: Optional[str] = None
    receivedSPF: Optional[str] = None
    authenticationResults: Optional[str] = None
    dKimsSignature: Optional[str] = None
    headersMessageId: Optional[str] = None
    mimeVersion: Optional[str] = None
    From: Optional[str] = None
    to: Optional[str] = None
    subject: Optional[str] = None
    date: Optional[str] = None
    headersListId: Optional[str] = None
    headersListUnsubscribe: Optional[str] = None
    precedence: Optional[str] = None
    xCsaComplaints: Optional[str] = None
    xMjMid: Optional[str] = None
    xMjMimeMessageStructure: Optional[str] = None
    feedbackId: Optional[str] = None
    contentType: Optional[str] = None
    size: Optional[str] = None
    body: Optional[str] = None
    mimeType: Optional[str] = None