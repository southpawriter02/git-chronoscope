# Slack Integration

## Implementation Status
**⏳ NOT IMPLEMENTED**

## 1. Feature Description

This feature provides a Slack bot that allows teams to generate and share git-chronoscope time-lapse videos directly within Slack channels.

## 2. Intended Functionality

- Slack slash command: `/chronoscope https://github.com/user/repo`
- Bot generates time-lapse and posts video to channel
- Interactive message buttons for configuration:
    - Format (MP4, GIF)
    - Date range
    - Branch selection
- Threaded progress updates during generation
- Integration with GitHub/GitLab OAuth for private repos

## 3. Requirements

- **Dependencies:**
    - Slack Bot API and OAuth
    - Message formatting and interactive components
    - File upload API for posting videos
- Slack App configuration and publishing
- Background job processing for long-running generations
- Rate limiting and queue management

## 4. Limitations

- Slack file size limits (typically 1GB for paid, less for free)
- Generation time may exceed Slack's 3-second response timeout (requires async)
- Private repository access requires OAuth configuration
- Bot installation requires workspace admin approval
