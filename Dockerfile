FROM python:3.11-slim

LABEL maintainer="git-chronoscope"
LABEL description="Generate time-lapse videos of Git repository history"

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

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
