import requests
import json

# Test the chat endpoint
def test_chat():
    url = "http://127.0.0.1:8000/chat"
    data = {
        "message": "Hello! What is artificial intelligence?",
        "conversation_history": [],
        "use_rag": False
    }
    
    response = requests.post(url, json=data)
    print("Status:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    test_chat()