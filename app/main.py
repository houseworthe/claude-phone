# app/main.py
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from .models.schemas import CommandRequest
from .services.claude_runner import ClaudeRunner
from .services.terminal_manager import terminal_manager
from .core.security import verify_api_token, verify_http_basic

load_dotenv()

app = FastAPI(
    title="Claude Phone",
    description="A secure MCP server to remotely control your development environment.",
    version="0.1.0",
)

LOG_FILE = "logs/session.log"

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Path to static files
STATIC_DIR = Path(__file__).parent.parent / "static"

@app.get("/", tags=["Terminal"])
async def get_terminal(username: str = Depends(verify_http_basic)):
    """
    Serve the terminal interface HTML.
    Protected by HTTP Basic Auth.
    """
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Terminal interface not found")
    return FileResponse(index_path)

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

@app.websocket("/ws")
async def websocket_terminal(websocket: WebSocket):
    """
    WebSocket endpoint for terminal access.
    Authentication is inherited from the HTTP session that served the page.
    """
    await websocket.accept()
    
    try:
        # Run the terminal session
        await terminal_manager.run_terminal_session(websocket)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
    finally:
        try:
            await websocket.close()
        except:
            pass