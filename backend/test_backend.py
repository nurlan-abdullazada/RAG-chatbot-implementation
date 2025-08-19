import requests
import json

# Test the API
def test_api():
    base_url = "http://localhost:8000"
    
    # Test health check
    response = requests.get(f"{base_url}/health")
    print("Health check:", response.json())
    
    # Test chat
    chat_data = {
        "message": "Hello! What is quantum computing?",
        "conversation_history": [],
        "use_rag": False
    }
    
    response = requests.post(f"{base_url}/chat", json=chat_data)
    print("Chat response:", response.json())

if __name__ == "__main__":
    test_api()