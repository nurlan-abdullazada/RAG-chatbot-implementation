import os
import streamlit as st
import requests
import json
from datetime import datetime
import time

# Configure Streamlit page
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


def init_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

def call_backend_api(message: str, use_rag: bool = True):
    """Call the FastAPI backend"""
    try:
        payload = {
            "message": message,
            "conversation_history": st.session_state.conversation_history,
            "use_rag": use_rag
        }
        
        response = requests.post(f"{BACKEND_URL}/test", timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            error_detail = response.json() if response.content else "No error details available"
            st.error(f"API Error {response.status_code}: {error_detail}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Make sure the FastAPI server is running!")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def add_message(role: str, content: str):
    """Add message to chat history"""
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now()
    }
    st.session_state.messages.append(message)
    
    # Update conversation history for API
    st.session_state.conversation_history.append({
        "role": role,
        "content": content
    })

def main():
    # Initialize session state
    init_session_state()
    
    # Header
    st.title("🤖 RAG Chatbot")
    st.markdown("Ask me anything! I'm powered by AWS Bedrock and Claude.")
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # Backend status check
        try:
            health_response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if health_response.status_code == 200:
                st.success("✅ Backend Connected")
                health_data = health_response.json()
                st.json(health_data)
            else:
                st.error("❌ Backend Error")
        except:
            st.error("❌ Backend Offline")
            st.warning("Start the backend with: `python run_backend.py`")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.conversation_history = []
            st.rerun()
        
        # RAG toggle
        use_rag = st.checkbox("Use RAG", value=True, help="Enable knowledge base retrieval")
    
    # Chat display
    st.subheader("💬 Chat")
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                st.caption(f"📅 {message['timestamp'].strftime('%H:%M:%S')}")
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message
        add_message("user", prompt)
        
        # Display user message immediately
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = call_backend_api(prompt, use_rag)
                
                if response:
                    bot_response = response.get("response", "Sorry, I couldn't generate a response.")
                    st.write(bot_response)
                    
                    # Add bot message to history
                    add_message("assistant", bot_response)
                    
                    # Show metadata
                    with st.expander("📊 Response Details"):
                        st.json({
                            "message_id": response.get("message_id"),
                            "model": response.get("model_used"),
                            "timestamp": response.get("timestamp")
                        })
                else:
                    error_msg = "❌ Failed to get response from backend."
                    st.error(error_msg)
                    add_message("assistant", error_msg)

if __name__ == "__main__":
    main()