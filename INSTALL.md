# Installation Guide

git-chronoscope can be installed through multiple methods. Choose the one that best fits your workflow.

## Prerequisites

All installation methods require:
- **FFmpeg** - Required for video encoding ([download](https://ffmpeg.org/download.html))
- **Git** - Required for repository access

## Quick Install

### PyPI (Recommended)

```bash
pip install git-chronoscope
```

### Homebrew (macOS/Linux)

```bash
brew tap southpawriter02/git-chronoscope
brew install git-chronoscope
```

### Docker

```bash
docker pull southpawriter02/git-chronoscope
```

---

## Detailed Installation Instructions

### Option 1: PyPI Package

The simplest way to install git-chronoscope is via pip:

```bash
# Install from PyPI
pip install git-chronoscope

# Or with a specific version
pip install git-chronoscope==0.9.0-beta.1

# Verify installation
git-chronoscope --help
```

**Requirements:**
- Python 3.7 or higher
- FFmpeg installed and in PATH

### Option 2: Homebrew (macOS/Linux)

Install using the Homebrew package manager:

```bash
# Add the tap (first time only)
brew tap southpawriter02/git-chronoscope

# Install
brew install git-chronoscope

# Update to latest version
brew update && brew upgrade git-chronoscope
```

Homebrew will automatically install Python and FFmpeg dependencies.

### Option 3: Standalone Executables

Pre-built executables are available for Windows, macOS, and Linux. No Python installation required.

1. Go to the [Releases page](https://github.com/southpawriter02/git-chronoscope/releases)
2. Download the appropriate file for your platform:
   - `git-chronoscope-windows.exe` - Windows
   - `git-chronoscope-macos` - macOS
   - `git-chronoscope-linux` - Linux
3. Make executable (macOS/Linux):
   ```bash
   chmod +x git-chronoscope-macos  # or git-chronoscope-linux
   ```
4. Run:
   ```bash
   ./git-chronoscope-macos /path/to/repo output.mp4
   ```

**Note:** You still need FFmpeg installed separately.

### Option 4: Docker

Run git-chronoscope in a container with all dependencies pre-installed:

```bash
# Pull the image
docker pull southpawriter02/git-chronoscope

# Run with a local repository
docker run -v /path/to/repo:/repo -v /path/to/output:/output \
  southpawriter02/git-chronoscope /repo /output/timelapse.mp4

# With additional options
docker run -v /path/to/repo:/repo -v /path/to/output:/output \
  southpawriter02/git-chronoscope /repo /output/timelapse.mp4 \
  --format gif --resolution 720p --fps 5
```

### Option 5: From Source

For development or to get the latest changes:

```bash
# Clone the repository
git clone https://github.com/southpawriter02/git-chronoscope.git
cd git-chronoscope

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run directly
python -m src.main /path/to/repo output.mp4

# Or install in development mode
pip install -e .
git-chronoscope /path/to/repo output.mp4
```

### Option 6: GitHub Actions

Use git-chronoscope directly in your CI/CD pipeline:

```yaml
- uses: southpawriter02/git-chronoscope@v1
  with:
    format: mp4
    output-path: timelapse.mp4
    resolution: 1080p
```

See [.github/workflows/timelapse.yml](.github/workflows/timelapse.yml) for a complete example.

---

## Verifying Installation

After installation, verify everything works:

```bash
# Check version
git-chronoscope --version

# Show help
git-chronoscope --help

# Test with a repository
git-chronoscope /path/to/any/git/repo test-output.mp4 --dry-run
```

---

## Troubleshooting

### FFmpeg not found

If you see "FFmpeg not found" errors:

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract and add the `bin` folder to your PATH

### Permission denied (macOS standalone)

```bash
chmod +x git-chronoscope-macos
xattr -d com.apple.quarantine git-chronoscope-macos  # Remove quarantine flag
```

### Python version issues

git-chronoscope requires Python 3.7+. Check your version:

```bash
python --version
# or
python3 --version
```

---

## Uninstalling

### PyPI
```bash
pip uninstall git-chronoscope
```

### Homebrew
```bash
brew uninstall git-chronoscope
brew untap southpawriter02/git-chronoscope
```

### Docker
```bash
docker rmi southpawriter02/git-chronoscope
```

---

## Next Steps

- Read the [README](README.md) for usage examples
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
