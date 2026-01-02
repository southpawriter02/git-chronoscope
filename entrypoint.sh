#!/bin/bash
set -e

# Arguments from action.yml
FORMAT="${1:-mp4}"
OUTPUT_PATH="${2:-timelapse.mp4}"
BRANCH="${3:-}"
RESOLUTION="${4:-1080p}"
FPS="${5:-2}"
INCLUDE="${6:-}"
EXCLUDE="${7:-}"
REDACT_SECRETS="${8:-false}"
AUTHOR_COLORS="${9:-false}"

# Build command
CMD="python -m src.main /github/workspace ${OUTPUT_PATH} --format ${FORMAT} --resolution ${RESOLUTION} --fps ${FPS}"

# Add optional branch
if [ -n "$BRANCH" ]; then
    CMD="$CMD --branch $BRANCH"
fi

# Add include patterns (comma-separated)
if [ -n "$INCLUDE" ]; then
    IFS=',' read -ra PATTERNS <<< "$INCLUDE"
    for pattern in "${PATTERNS[@]}"; do
        CMD="$CMD --include \"$pattern\""
    done
fi

# Add exclude patterns (comma-separated)
if [ -n "$EXCLUDE" ]; then
    IFS=',' read -ra PATTERNS <<< "$EXCLUDE"
    for pattern in "${PATTERNS[@]}"; do
        CMD="$CMD --exclude \"$pattern\""
    done
fi

# Add redact-secrets flag
if [ "$REDACT_SECRETS" = "true" ]; then
    CMD="$CMD --redact-secrets"
fi

# Add author-colors flag
if [ "$AUTHOR_COLORS" = "true" ]; then
    CMD="$CMD --author-colors"
fi

echo "Running: $CMD"
eval $CMD

# Set output for GitHub Actions
echo "output-file=${OUTPUT_PATH}" >> $GITHUB_OUTPUT
