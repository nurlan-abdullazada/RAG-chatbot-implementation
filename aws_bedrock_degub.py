import boto3
from config import config

client = boto3.client(
    "bedrock-runtime",
    region_name=config.AWS_REGION,
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
)

# List all available models
try:
    bedrock_client = boto3.client("bedrock", region_name=config.AWS_REGION,
                                 aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)
    
    models = bedrock_client.list_foundation_models()
    print("Available Claude models:")
    
    for model in models['modelSummaries']:
        if 'claude' in model['modelId'].lower():
            print(f"✅ {model['modelId']}")
            
except Exception as e:
    print(f"Error: {e}")