# Contributing to Claude Phone

Thank you for your interest in contributing! We're excited to build a powerful open-source tool with the help of the community.

## How to Contribute

We welcome contributions of all kinds, from bug reports to feature proposals and pull requests.

### Reporting Bugs

If you encounter a bug, please open an issue on our GitHub repository. Please include:
- A clear and descriptive title.
- A detailed description of the problem, including steps to reproduce it.
- Any relevant logs or error messages.
- Your environment details (OS, Python version, etc.).

### Suggesting Enhancements

Have an idea for a new feature or an improvement to an existing one? Open an issue and use the "Feature Request" template. We'd love to hear your thoughts.

### Pull Requests

We welcome pull requests! To ensure a smooth process, please follow these steps:

1.  **Fork the repository** and create your branch from `main`.
2.  **Make your changes.** Please ensure your code adheres to our style guidelines.
3.  **Add tests** for any new features or bug fixes. (Testing framework to be established).
4.  **Update the documentation** if you are changing any user-facing behavior.
5.  **Ensure your PR is focused.** Please submit one feature or bug fix per PR.
6.  **Submit the pull request** with a clear description of the changes you've made.

## Development Setup

### Backend Development

1.  Clone the repository: `git clone https://github.com/your-username/claude-phone.git`
2.  Create a virtual environment: `python -m venv venv`
3.  Activate it: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
4.  Install dependencies: `pip install -r requirements.txt`
5.  Set up your `.env` file from `.env.example`:
    ```bash
    cp .env.example .env
    # Edit .env with your preferred credentials
    ```
6.  Run the development server: `uvicorn app.main:app --reload`

### Frontend Development

The frontend is a single `static/index.html` file using xterm.js. To modify:

1.  Edit `static/index.html` directly
2.  Test changes by refreshing your browser
3.  Ensure the terminal properly connects to the WebSocket endpoint

### Testing with Docker

```bash
# Build the Docker image
docker build -t claude-phone-dev .

# Run with your .env file
docker run -p 8000:8000 --env-file .env claude-phone-dev
```

### Code Style

- **Python**: Follow PEP 8 conventions
- **JavaScript**: Use modern ES6+ syntax
- **HTML/CSS**: Keep it clean and semantic
- **Comments**: Write clear, concise comments for complex logic

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior. (A formal `CODE_OF_CONDUCT.md` will be added shortly).

We look forward to building with you!