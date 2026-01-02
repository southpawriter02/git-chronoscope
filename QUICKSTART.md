# Quick Start

Generate your first time-lapse in 5 minutes.

## 1. Install

```bash
# Clone
git clone https://github.com/user/git-chronoscope.git
cd git-chronoscope

# Install dependencies
pip install -r requirements.txt
```

## 2. Prerequisites

- Git installed
- FFmpeg installed (for video output)

## 3. Generate Time-Lapse

```bash
# Basic usage
python -m src.main /path/to/your/repo output.mp4

# With options
python -m src.main /path/to/repo output.mp4 --fps 10 --resolution 1080p
```

## 4. View Result

Open `output.mp4` to see your repository's evolution!

## Common Options

| Option | Description |
|--------|-------------|
| `--fps 10` | Frames per second |
| `--resolution 1080p` | Video resolution |
| `--format gif` | Output as GIF |
| `--include "*.py"` | Filter files |
| `--dry-run` | Preview without generating |

## Next Steps

- See `README.md` for full documentation
- See `TROUBLESHOOTING.md` if you encounter issues
