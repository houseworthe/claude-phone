# app/main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import StreamingResponse

from .models.schemas import CommandRequest
from .services.claude_runner import ClaudeRunner
from .core.security import verify_api_token

load_dotenv()

app = FastAPI(
    title="Claude Phone",
    description="A secure MCP server to remotely control your development environment.",
    version="0.1.0",
)

LOG_FILE = "logs/session.log"

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

@app.get("/status", tags=["Health"])
async def status():
    """A simple health check endpoint."""
    return {"status": "ok", "version": app.version}

@app.post("/execute", tags=["Commands"])
async def execute(
    request: CommandRequest,
    is_authenticated: bool = Depends(verify_api_token)
):
    """
    Execute a Claude Code CLI command and stream the output.
    
    Requires 'Authorization: Bearer <token>' header.
    """
    if not is_authenticated:
        # This check is redundant due to Depends raising an exception,
        # but serves as an explicit guard.
        raise HTTPException(status_code=401, detail="Unauthorized")

    runner = ClaudeRunner()

    async def stream_and_log():
        with open(LOG_FILE, "a") as log_file:
            async for line in runner.execute_command(request.prompt, request.repo_path, request.args):
                log_file.write(line + "\n")
                log_file.flush()
                yield line + "\n"

    return StreamingResponse(stream_and_log(), media_type="text/plain")

@app.get("/logs", tags=["Logs"])
async def get_logs(
    is_authenticated: bool = Depends(verify_api_token)
):
    """
    Retrieve the session log file.
    
    Requires 'Authorization: Bearer <token>' header.
    """
    if not os.path.exists(LOG_FILE):
        return {"message": "Log file not found."}
    
    with open(LOG_FILE, "r") as f:
        return StreamingResponse(f, media_type="text/plain")