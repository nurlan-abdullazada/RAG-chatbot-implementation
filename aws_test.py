# Create aws_test.py
import boto3
from config import config

try:
    client = boto3.client(
        "bedrock-runtime",
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    )
    
    # Test connection
    print("✅ AWS credentials loaded")
    print(f"Region: {config.AWS_REGION}")
    print(f"Access Key starts with: {config.AWS_ACCESS_KEY_ID[:10]}...")
    
    # Test Bedrock access (simple call)
    response = client.list_foundation_models()
    print("✅ Bedrock access successful!")
    
except Exception as e:
    print(f"❌ AWS Error: {e}")