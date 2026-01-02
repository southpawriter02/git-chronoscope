# Git Chronoscope VSCode Extension

Generate time-lapse visualizations of your Git repository directly in VSCode.

## Features

- **Generate Time-Lapse**: Create a video showing your repository's evolution
- **File-Specific Time-Lapse**: Focus on a single file's history
- **Sidebar Panel**: Easy access to generation controls
- **Output Channel**: Detailed logging for debugging

## Commands

| Command | Description |
|---------|-------------|
| `Chronoscope: Generate Time-Lapse` | Generate for entire repository |
| `Chronoscope: Generate Time-Lapse for Current File` | Generate for active file |
| `Chronoscope: Show Output` | Show logging output |

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `chronoscope.pythonPath` | `python3` | Path to Python executable |
| `chronoscope.outputFormat` | `mp4` | Default output format |
| `chronoscope.fps` | `5` | Frames per second |

## Requirements

- Python 3.7+
- git-chronoscope installed
- FFmpeg (for video output)

## Installation

1. Open VSCode Extensions (Ctrl+Shift+X)
2. Search for "Git Chronoscope"
3. Click Install

## Development

```bash
cd vscode-extension
npm install
npm run compile
npm test
```
