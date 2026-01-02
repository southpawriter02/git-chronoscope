FROM python:3.11-slim

LABEL maintainer="git-chronoscope"
LABEL description="Generate time-lapse videos of Git repository history"
LABEL org.opencontainers.image.source="https://github.com/southpawriter02/git-chronoscope"
LABEL org.opencontainers.image.version="0.9.0-beta.1"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application code
COPY requirements.txt .
COPY src/ ./src/
COPY templates/ ./templates/
COPY static/ ./static/
COPY entrypoint.sh .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Healthcheck - verify git-chronoscope can run
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from src.main import main; print('OK')" || exit 1

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
