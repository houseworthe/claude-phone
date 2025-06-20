# Claude Phone 📱

**Control your development environment from anywhere, using natural language.**

Claude Phone is a secure, self-hosted MCP (Model Context Protocol) server that acts as a remote control for AI code assistants like Anthropic's Claude Code CLI. It allows you to safely execute commands, run tests, refactor code, and interact with your git repositories from any device, turning your phone into a powerful development tool.

## The Problem

Modern AI coding tools are powerful but are often tethered to a local terminal session. How do you kick off a complex refactoring job while you're on the train? How do you check the status of your tests from your phone?

## The Solution

Claude Phone provides a simple, secure API layer on top of your command-line tools. It receives structured commands, executes them in a secure environment, and streams the real-time output back to you.

- **💡 Natural Language Control:** "Refactor `utils.py` to be more readable."
- **⚡️ Real-Time Feedback:** Watch the terminal output stream to your phone as commands run.
- **🔒 Secure by Design:** Uses bearer token authentication and runs in an isolated environment.
- **🌐 Accessible Anywhere:** Deployable to a free cloud service for a permanent, public URL.
- **📦 Open Source:** A free, community-driven tool designed to be extended and improved.

## Project Status

**Current Phase:** **Initial Development**. We are currently building the core MVP. The goal is a robust, secure, and easy-to-deploy server that can execute commands and stream results.

This project is under active development.

## Getting Involved

We believe in the power of open source. If you're interested in building the future of remote AI-assisted development, we welcome contributions. Please see `CONTRIBUTING.md` for more details.

---
*This is an independent project and is not officially affiliated with Anthropic.*