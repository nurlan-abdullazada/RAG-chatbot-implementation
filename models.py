from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant" 
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    conversation_history: List[ChatMessage] = []
    use_rag: bool = True
    temperature: Optional[float] = None

class ChatResponse(BaseModel):
    response: str
    message_id: str
    timestamp: datetime
    model_used: str = None
    
    class Config:
        protected_namespaces = ()
    
class StreamChunk(BaseModel):
    chunk: str
    is_complete: bool = False