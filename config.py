import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # AWS Configuration
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY") 
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    
    # Application Configuration
    BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))
    
    # LLM Configuration
    CLAUDE_MODEL_ID = os.getenv("CLAUDE_MODEL_ID", "us.anthropic.claude-3-7-sonnet-20250219-v1:0")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 4096))
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
    
    @classmethod
    def validate_config(cls):
        """Check if required environment variables are set"""
        required_vars = [
            cls.AWS_ACCESS_KEY_ID,
            cls.AWS_SECRET_ACCESS_KEY
        ]
        
        if not all(required_vars):
            raise ValueError("Missing required AWS credentials in .env file")
        
        return True

# Create a config instance
config = Config()