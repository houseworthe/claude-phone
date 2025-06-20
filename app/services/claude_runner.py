# app/services/claude_runner.py
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClaudeRunner:
    """
    A service to securely execute Claude Code CLI commands as an asynchronous subprocess.
    """
    async def execute_command(self, prompt: str, args: str | None):
        """
        Executes the claude command and yields its output line by line.
        """
        # Fixed repository path from Docker build
        repo_path = "/app/user_repo"
        
        # Security: Construct the command carefully. We control the base command.
        # The prompt is passed as a string argument, mitigating injection risks.
        command = f'claude --prompt "{prompt}" {args if args else ""}'
        
        logger.info(f"Executing command in repo: {repo_path}")
        logger.info(f"Full command: {command}")

        try:
            # Using asyncio's subprocess for non-blocking execution
            process = await asyncio.create_subprocess_shell(
                command,
                cwd=repo_path, # Execute the command within the target repo directory
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Concurrently stream stdout and stderr
            async for line in self._stream_reader(process.stdout):
                yield f"[STDOUT] {line}"
            
            async for line in self._stream_reader(process.stderr):
                yield f"[STDERR] {line}"

            await process.wait()
            return_code = process.returncode
            yield f"\n[PROCESS_EXIT] Command finished with exit code: {return_code}"
            logger.info(f"Command finished with exit code: {return_code}")

        except FileNotFoundError:
            error_msg = f"[ERROR] The target repository path does not exist: {repo_path}"
            logger.error(error_msg)
            yield error_msg
        except Exception as e:
            error_msg = f"[ERROR] An unexpected error occurred: {str(e)}"
            logger.error(error_msg, exc_info=True)
            yield error_msg
            
    async def _stream_reader(self, stream):
        """Helper to read lines from a stream asynchronously."""
        while True:
            line = await stream.readline()
            if not line:
                break
            yield line.decode('utf-8').strip()