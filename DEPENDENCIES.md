# Dependencies

This document lists all dependencies required by git-chronoscope.

## System Dependencies

### Git
```bash
# macOS
brew install git

# Ubuntu/Debian
sudo apt-get install git

# Windows
winget install Git.Git
```

### FFmpeg (for video output)
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
winget install FFmpeg.FFmpeg
```

## Python Dependencies

Install via pip:
```bash
pip install -r requirements.txt
```

| Package | Purpose |
|---------|---------|
| `GitPython` | Git repository interaction |
| `Pillow` | Frame image generation |
| `Pygments` | Syntax highlighting |
| `tqdm` | Progress bars (optional) |

## Quick Start

```bash
# Clone and install
git clone https://github.com/user/git-chronoscope.git
cd git-chronoscope
pip install -r requirements.txt

# Verify
python -m src.main --help
```

## Docker (Alternative)

```bash
docker build -t git-chronoscope .
docker run -v /path/to/repo:/repo git-chronoscope /repo output.mp4
```
