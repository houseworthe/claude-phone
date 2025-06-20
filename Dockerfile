# syntax=docker/dockerfile:1
# Stage 1: Clone the private repository
FROM python:3.11 as cloner

# Install git and SSH client
RUN apt-get update && apt-get install -y \
    git \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Accept build argument for the repository URL
ARG GIT_REPO_URL

# Set up SSH for cloning
RUN mkdir -p /root/.ssh && \
    ssh-keyscan -t rsa github.com >> /root/.ssh/known_hosts && \
    ssh-keyscan -t rsa gitlab.com >> /root/.ssh/known_hosts && \
    ssh-keyscan -t rsa bitbucket.org >> /root/.ssh/known_hosts

WORKDIR /app

# Clone the repository using the mounted secret SSH key
# This requires Docker BuildKit and the secret to be passed during build
RUN --mount=type=secret,id=git_ssh_key,mode=0600 \
    mkdir -p /root/.ssh && \
    cp /run/secrets/git_ssh_key /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa && \
    git clone ${GIT_REPO_URL} /app/user_repo && \
    rm -f /root/.ssh/id_rsa

# Stage 2: Build the final image without the SSH key
FROM python:3.11

# Set working directory
WORKDIR /app

# Install system dependencies and Node.js
RUN apt-get update && apt-get install -y \
    # Git for repository operations
    git \
    # Process management utilities
    procps \
    # curl for downloading
    curl \
    # Clean up apt cache to reduce image size
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20.x
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install Claude Code CLI globally
RUN npm install -g @anthropic-ai/claude-code

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app app/
COPY static static/

# Copy the cloned repository from the first stage
COPY --from=cloner /app/user_repo /app/user_repo

# Create logs directory
RUN mkdir -p logs

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]