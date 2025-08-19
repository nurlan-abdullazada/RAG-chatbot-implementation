# run_backend.py
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn
from config import config

if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # This should work now
        host="127.0.0.1",  # Change to localhost for local testing
        port=8000,
        reload=True
    )