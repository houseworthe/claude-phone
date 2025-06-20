# Claude Phone 📱

**A secure, browser-based terminal for remote development—control your entire development environment from any device.**

Claude Phone is a self-hosted web application that provides real-time terminal access to your development environment through any web browser. Whether you're using Claude Code CLI, running tests, or managing your git repositories, Claude Phone turns any device into a powerful development workstation.

## The Problem

Modern developers need access to their development environment from anywhere. Whether you're debugging on your phone during a commute, running tests from a tablet, or executing AI-assisted refactoring from a friend's computer, you need secure, real-time access to your tools.

## The Solution

Claude Phone provides two powerful interfaces:

### 🖥️ Interactive Terminal (Primary Interface)
A full-featured browser-based terminal powered by WebSockets and xterm.js:
- **Real Bash Shell:** Complete terminal access with PTY emulation
- **Real-Time Interaction:** Type commands and see results instantly
- **Mobile Optimized:** Works beautifully on phones and tablets
- **Secure Access:** HTTP Basic Auth protects your terminal

### 🚀 REST API (Advanced Usage)
Programmatic access for automation and integrations:
- **Natural Language Commands:** Send prompts to Claude Code CLI
- **Streaming Responses:** Get real-time command output
- **Bearer Token Auth:** Secure API access for scripts

## Key Features

- **🔐 Security First:** Multiple authentication methods, isolated processes
- **⚡ Real-Time Communication:** WebSocket-based terminal, streaming API responses
- **📱 Mobile Friendly:** Responsive design works on any device
- **🐳 Easy Deployment:** Docker container ready for cloud platforms
- **🛠️ Extensible:** Clean architecture for customization

## Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/claude-phone.git
cd claude-phone

# Create .env file from example
cp .env.example .env
# Edit .env to set your credentials

# Build and run with Docker
docker build -t claude-phone .
docker run -p 8000:8000 --env-file .env claude-phone
```

Access the terminal at `http://localhost:8000` (login with your configured credentials).

### Manual Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env file

# Run the server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Configuration

Create a `.env` file with the following variables:

```env
# Terminal Access (HTTP Basic Auth)
CP_USER=your_username
CP_PASSWORD=your_secure_password

# API Access (Bearer Token)
CLAUDE_PHONE_API_TOKEN=your_api_token_here
```

### Using with a Private Repository

Claude Phone can securely clone and work with your private Git repositories using SSH deploy keys. This feature ensures your code remains secure while giving Claude Phone the access it needs.

#### Step 1: Generate an SSH Key Pair

First, create a new SSH key specifically for this deployment:

```bash
# Generate a new SSH key (do not set a passphrase)
ssh-keygen -t ed25519 -C "claude-phone-deploy" -f ~/.ssh/claude-phone-deploy

# This creates two files:
# - claude-phone-deploy (private key)
# - claude-phone-deploy.pub (public key)
```

**Important:** When prompted for a passphrase, press Enter twice to create a key without a passphrase.

#### Step 2: Add Deploy Key to Your Repository

1. Copy the contents of the public key:
   ```bash
   cat ~/.ssh/claude-phone-deploy.pub
   ```

2. Go to your GitHub repository's settings:
   - Navigate to `Settings` → `Deploy keys`
   - Click `Add deploy key`
   - Title: "Claude Phone Access"
   - Key: Paste the public key contents
   - Check "Allow write access" if Claude Phone needs to push changes
   - Click `Add key`

For other platforms:
- **GitLab:** Settings → Repository → Deploy Keys
- **Bitbucket:** Repository settings → Access keys

#### Step 3: Configure Your Cloud Provider

##### Railway

1. In your Railway project dashboard:
   - Go to your service settings
   - Navigate to the "Variables" tab
   - Add a new variable:
     - Name: `GIT_REPO_URL`
     - Value: `git@github.com:your-username/your-private-repo.git`
   
2. Add the private key as a secret:
   - Railway doesn't directly support build secrets yet
   - Use a build argument instead (see alternative method below)

##### Render

1. In your Render service dashboard:
   - Go to "Environment" tab
   - Add environment variable:
     - Key: `GIT_REPO_URL`
     - Value: `git@github.com:your-username/your-private-repo.git`

2. Add the private key:
   - Create a secret file named `git_ssh_key`
   - Paste the contents of your private key file

##### Alternative: Using Build Arguments

If your platform doesn't support Docker BuildKit secrets, you can modify the build command:

```bash
# Read the private key and pass it as a build argument
docker build \
  --build-arg GIT_REPO_URL="git@github.com:your-username/your-private-repo.git" \
  --secret id=git_ssh_key,src=~/.ssh/claude-phone-deploy \
  -t claude-phone .
```

#### Step 4: Deploy with Docker BuildKit

When building locally with Docker, use BuildKit to securely pass the SSH key:

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Build with the secret
docker build \
  --build-arg GIT_REPO_URL="git@github.com:your-username/your-private-repo.git" \
  --secret id=git_ssh_key,src=~/.ssh/claude-phone-deploy \
  -t claude-phone .
```

#### Security Notes

- **Never commit SSH keys to your repository**
- The private key is only used during the build process
- The multi-stage Dockerfile ensures the key is not present in the final image
- Your repository is cloned to `/app/user_repo` inside the container
- Each deployment should use a unique deploy key for audit trails

#### Troubleshooting

If the clone fails:
1. Verify the SSH URL is correct (use `git@github.com:...` not `https://...`)
2. Ensure the deploy key has read access to the repository
3. Check that the private key file has correct permissions (`chmod 600`)
4. Test the key locally: `ssh -i ~/.ssh/claude-phone-deploy -T git@github.com`

## Usage

### Terminal Interface

1. Open your browser to `http://your-server:8000`
2. Log in with your configured username and password
3. You now have a full terminal in your browser!

```bash
# Run any command
ls -la

# Use Claude Code CLI
claude --prompt "refactor the utils.py file to improve readability"

# Run tests
pytest

# Git operations
git status
git commit -m "Fixed bug in authentication"
```

### REST API

For programmatic access, use the API endpoints:

```bash
# Execute a command
curl -X POST http://your-server:8000/execute \
  -H "Authorization: Bearer your_api_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "analyze the security of auth.py",
    "args": "--yes"
  }'

# Check server status
curl http://your-server:8000/status

# Get logs
curl -H "Authorization: Bearer your_api_token_here" \
  http://your-server:8000/logs
```

## Deployment

### Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/)

### Deploy to Render

1. Fork this repository
2. Create a new Web Service on Render
3. Connect your forked repo
4. Set environment variables (CP_USER, CP_PASSWORD, CLAUDE_PHONE_API_TOKEN)
5. Deploy!

## Architecture

Claude Phone uses a modular architecture:

- **FastAPI Backend:** High-performance async Python server
- **WebSocket + PTY:** Real-time terminal emulation
- **xterm.js Frontend:** Professional terminal rendering
- **Docker:** Consistent deployment across platforms

## Security Considerations

- Always use strong passwords for CP_USER and CP_PASSWORD
- Keep your CLAUDE_PHONE_API_TOKEN secret
- Use HTTPS in production (reverse proxy recommended)
- Run in a container or VM for process isolation
- Regularly update dependencies

## Project Status

**Current Phase:** **Active Development**

- ✅ Core REST API with streaming
- ✅ WebSocket terminal implementation
- ✅ Docker containerization
- ✅ Mobile-responsive interface
- 🚧 Advanced authentication options
- 🚧 Session management
- 🚧 Multi-user support

## Getting Involved

We believe in the power of open source. If you're interested in building the future of remote development tools, we welcome contributions! Please see `CONTRIBUTING.md` for more details.

## License

MIT License - see LICENSE file for details.

---
*This is an independent project and is not officially affiliated with Anthropic.*