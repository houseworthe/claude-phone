# app/core/security.py
import os
import secrets
from dotenv import load_dotenv
from fastapi import HTTPException, Security, Depends, status
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials

load_dotenv()

API_TOKEN_NAME = "Authorization"
API_TOKEN_HEADER = APIKeyHeader(name=API_TOKEN_NAME, auto_error=True)

# Bearer token for API access
CLAUDE_PHONE_API_TOKEN = os.getenv("CLAUDE_PHONE_API_TOKEN")

if not CLAUDE_PHONE_API_TOKEN:
    raise ValueError("CLAUDE_PHONE_API_TOKEN environment variable not set!")

# HTTP Basic Auth credentials for terminal access
CP_USER = os.getenv("CP_USER")
CP_PASSWORD = os.getenv("CP_PASSWORD")

if not CP_USER or not CP_PASSWORD:
    raise ValueError("CP_USER and CP_PASSWORD environment variables must be set!")

# HTTP Basic security instance
security = HTTPBasic()

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

async def verify_http_basic(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Verifies HTTP Basic authentication credentials for terminal access.
    """
    is_username_correct = secrets.compare_digest(credentials.username, CP_USER)
    is_password_correct = secrets.compare_digest(credentials.password, CP_PASSWORD)
    
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username