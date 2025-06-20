# app/core/security.py
import os
from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

load_dotenv()

API_TOKEN_NAME = "Authorization"
API_TOKEN_HEADER = APIKeyHeader(name=API_TOKEN_NAME, auto_error=True)

# It's recommended to set this in your deployment environment variables
CLAUDE_PHONE_API_TOKEN = os.getenv("CLAUDE_PHONE_API_TOKEN")

if not CLAUDE_PHONE_API_TOKEN:
    raise ValueError("CLAUDE_PHONE_API_TOKEN environment variable not set!")

async def verify_api_token(api_token: str = Security(API_TOKEN_HEADER)):
    """
    Verifies that the provided API token matches the server's secret token.
    The token should be provided as 'Bearer <token>'.
    """
    if not api_token.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid token format. Use 'Bearer <token>'.")
    
    token = api_token.split(" ")[1]

    if token != CLAUDE_PHONE_API_TOKEN:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return True