# Discord Bot

## Implementation Status
**⏳ NOT IMPLEMENTED**

## 1. Feature Description

This feature provides a Discord bot that enables developers and communities to generate git-chronoscope time-lapses within Discord servers.

## 2. Intended Functionality

- Bot command: `!chronoscope https://github.com/user/repo`
- Slash commands: `/chronoscope generate <repo_url>`
- Video posted directly to channel after generation
- Embed with video preview, repository info, and stats
- Configuration options via command flags:
    - `--format gif` or `--format mp4`
    - `--branch main`
    - `--days 30`

## 3. Requirements

- **Dependencies:**
    - Discord.py or discord.js bot framework
    - Discord Application and Bot Token
    - File attachment handling
- Application registration with Discord
- Background processing for generation
- Hosting for bot runtime

## 4. Limitations

- Discord file upload limit (25MB for free servers, 100MB with Nitro)
- Large time-lapses may need to be compressed or linked externally
- Bot needs to be added to each server individually
- Rate limits on Discord API
