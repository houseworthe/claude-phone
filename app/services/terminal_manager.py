# app/services/terminal_manager.py
import asyncio
import logging
import ptyprocess
from fastapi import WebSocket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TerminalManager:
    """
    Manages PTY (pseudo-terminal) processes for WebSocket connections.
    Each WebSocket connection gets its own isolated bash shell.
    """
    
    async def run_terminal_session(self, websocket: WebSocket):
        """
        Run an interactive terminal session over a WebSocket connection.
        
        Args:
            websocket: The WebSocket connection to communicate through
        """
        pty_process = None
        
        try:
            # Spawn a new bash shell with PTY
            pty_process = ptyprocess.PtyProcess.spawn(['bash'])
            logger.info(f"Started PTY process with PID: {pty_process.pid}")
            
            # Create tasks for bidirectional communication
            read_task = asyncio.create_task(self._read_pty_output(pty_process, websocket))
            write_task = asyncio.create_task(self._write_pty_input(pty_process, websocket))
            
            # Wait for either task to complete (usually due to disconnection)
            done, pending = await asyncio.wait(
                [read_task, write_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel the remaining task
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
                    
        except Exception as e:
            logger.error(f"Terminal session error: {str(e)}", exc_info=True)
            
        finally:
            # Ensure PTY process is terminated
            if pty_process and pty_process.isalive():
                logger.info(f"Terminating PTY process {pty_process.pid}")
                try:
                    pty_process.terminate(force=True)
                except:
                    pass
    
    async def _read_pty_output(self, pty_process: ptyprocess.PtyProcess, websocket: WebSocket):
        """
        Read output from PTY and send to WebSocket.
        """
        try:
            while True:
                # Read from PTY (with timeout to allow checking if process is alive)
                try:
                    output = await asyncio.get_event_loop().run_in_executor(
                        None, 
                        lambda: pty_process.read(1024)
                    )
                    if output:
                        await websocket.send_text(output.decode('utf-8', errors='replace'))
                except EOFError:
                    # PTY closed
                    logger.info("PTY process ended")
                    break
                except Exception as e:
                    logger.error(f"Error reading from PTY: {str(e)}")
                    break
                    
                # Small delay to prevent CPU spinning
                await asyncio.sleep(0.01)
                
        except Exception as e:
            logger.error(f"PTY read task error: {str(e)}")
    
    async def _write_pty_input(self, pty_process: ptyprocess.PtyProcess, websocket: WebSocket):
        """
        Read input from WebSocket and write to PTY.
        """
        try:
            while True:
                # Receive data from WebSocket
                data = await websocket.receive_text()
                
                # Write to PTY
                await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: pty_process.write(data.encode('utf-8'))
                )
                
        except Exception as e:
            # WebSocket disconnected or error
            logger.info(f"WebSocket disconnected: {str(e)}")

# Global instance for easy access
terminal_manager = TerminalManager()