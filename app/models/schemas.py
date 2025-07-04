# app/models/schemas.py
from pydantic import BaseModel, Field

class CommandRequest(BaseModel):
    """
    Defines the structure for an incoming command request.
    """
    prompt: str = Field(
        ...,
        description="The natural language prompt or full command to be executed by Claude Code CLI.",
        examples=["Refactor services/claude_runner.py to add more robust error handling."]
    )
    args: str | None = Field(
        default="--yes",
        description="Optional additional arguments to pass to the Claude Code CLI.",
        examples=["--yes --verbose"]
    )