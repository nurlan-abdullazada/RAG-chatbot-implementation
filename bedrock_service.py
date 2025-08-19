import boto3
import json
import uuid
from datetime import datetime
from typing import List, Dict, Iterator
from config import config
from models import ChatMessage

class BedrockService:
    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=config.AWS_REGION,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        )
        self.model_id = config.CLAUDE_MODEL_ID
    
    def create_body_json(self, messages: List[Dict], system: str = None, temperature: float = None):
        """Create request body for Claude API (from your notebook)"""
        body_dict = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": config.MAX_TOKENS,
            "temperature": temperature or config.TEMPERATURE,
            "messages": messages,
        }
        
        if system:
            body_dict["system"] = system
            
        return json.dumps(body_dict)
    
    def format_conversation_history(self, history: List[ChatMessage]) -> List[Dict]:
        """Convert ChatMessage objects to Claude API format"""
        formatted_messages = []
        for msg in history:
            formatted_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        return formatted_messages
    
    def chat_completion(self, message: str, conversation_history: List[ChatMessage] = None, system: str = None, temperature: float = None) -> str:
        """Get a complete response from Claude"""
        messages = []
        
        # Add conversation history
        if conversation_history:
            messages.extend(self.format_conversation_history(conversation_history))
        
        # Add current user message
        messages.append({
            "role": "user", 
            "content": message
        })
        
        # Create request body
        body_json = self.create_body_json(messages, system, temperature)
        
        # Make API call
        response = self.client.invoke_model(
            modelId=self.model_id,
            contentType="application/json",
            accept="application/json",
            body=body_json
        )
        
        # Parse response
        response_body = json.loads(response['body'].read().decode('utf-8'))
        return response_body['content'][0]['text']
    
    def chat_completion_stream(self, message: str, conversation_history: List[ChatMessage] = None, system: str = None, temperature: float = None) -> Iterator[str]:
        """Get streaming response from Claude (from your notebook)"""
        messages = []
        
        # Add conversation history
        if conversation_history:
            messages.extend(self.format_conversation_history(conversation_history))
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": message
        })
        
        # Create request body
        body_json = self.create_body_json(messages, system, temperature)
        
        # Make streaming API call
        stream = self.client.invoke_model_with_response_stream(
            modelId=self.model_id,
            contentType="application/json",
            accept="application/json",
            body=body_json
        )
        
        # Process stream (from your notebook)
        stream_body = stream.get("body")
        for event in stream_body:
            stream_chunk = event.get("chunk")
            if stream_chunk:
                decoded = json.loads(stream_chunk.get("bytes").decode("utf-8"))
                delta = decoded.get("delta", {})
                text = delta.get("text", "")
                if text:
                    yield text