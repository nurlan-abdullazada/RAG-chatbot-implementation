from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json
import uuid
from datetime import datetime

# Import our custom modules - absolute imports
from models import ChatRequest, ChatResponse, ChatMessage
from bedrock_service import BedrockService
from config import config


# Create FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="A RAG-based chatbot using AWS Bedrock",
    version="1.0.0"
)

# Enable CORS (so frontend can talk to backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, be more specific
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Bedrock service
bedrock_service = BedrockService()

@app.on_event("startup")
async def startup_event():
    """Validate configuration on startup"""
    try:
        config.validate_config()
        print("✅ AWS configuration validated successfully")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        raise

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "RAG Chatbot API is running!",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model": config.CLAUDE_MODEL_ID,
        "region": config.AWS_REGION,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    """Non-streaming chat endpoint"""
    try:
        # Get response from Bedrock
        response_text = bedrock_service.chat_completion(
            message=request.message,
            conversation_history=request.conversation_history,
            temperature=request.temperature
        )
        
        # Create response
        chat_response = ChatResponse(
            response=response_text,
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            model_used=config.CLAUDE_MODEL_ID
        )
        
        return chat_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint"""
    try:
        def generate_stream():
            # Send initial metadata
            yield f"data: {json.dumps({'type': 'start', 'message_id': str(uuid.uuid4())})}\n\n"
            
            # Stream the response
            for chunk in bedrock_service.chat_completion_stream(
                message=request.message,
                conversation_history=request.conversation_history,
                temperature=request.temperature
            ):
                chunk_data = {
                    'type': 'chunk',
                    'content': chunk
                }
                yield f"data: {json.dumps(chunk_data)}\n\n"
            
            # Send completion signal
            yield f"data: {json.dumps({'type': 'end'})}\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error streaming response: {str(e)}")

@app.get("/conversations")
async def get_conversations():
    """Get conversation history (placeholder for now)"""
    return {"conversations": []}

@app.post("/test")
async def test_endpoint():
    """Simple test without AWS"""
    return {
        "response": "Hello! This is a test response without AWS.",
        "message_id": str(uuid.uuid4()),
        "timestamp": datetime.now(),
        "model_used": "test"
    }

# At the bottom of main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,  # Use app directly, not "main:app"
        host="127.0.0.1",  # Use localhost
        port=8000,
        reload=True
    )