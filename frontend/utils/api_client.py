import requests
import streamlit as st
from typing import Dict, List, Optional

class ChatbotAPIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
    
    def health_check(self) -> Dict:
        """Check if backend is healthy"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return {
                "status": "healthy" if response.status_code == 200 else "error",
                "data": response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            return {"status": "offline", "error": str(e)}
    
    def send_message(self, message: str, history: List[Dict] = None, use_rag: bool = True) -> Optional[Dict]:
        """Send message to chatbot"""
        try:
            payload = {
                "message": message,
                "conversation_history": history or [],
                "use_rag": use_rag
            }
            
            response = requests.post(
                f"{self.base_url}/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API Error: {response.status_code}")
                return None
                
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None