# git-chronoscope

[![npm version](https://badge.fury.io/js/git-chronoscope.svg)](https://badge.fury.io/js/git-chronoscope)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Generate time-lapse visualizations of Git repository evolution.

This is the official npm wrapper for [git-chronoscope](https://github.com/southpawriter02/git-chronoscope). It provides both a CLI and a programmatic API for Node.js.

## Prerequisites

This package requires the following to be installed:

- **Python 3.7+** - [Download](https://www.python.org/downloads/)
- **git-chronoscope Python package** - `pip install git-chronoscope`
- **FFmpeg** - [Download](https://ffmpeg.org/download.html)
- **Git** - [Download](https://git-scm.com/downloads)

## Installation

```bash
# Global installation (recommended for CLI usage)
npm install -g git-chronoscope

# Project dependency
npm install git-chronoscope

# Or use without installing
npx git-chronoscope
```

## CLI Usage

```bash
# Basic usage
git-chronoscope /path/to/repo output.mp4

# Generate a GIF
git-chronoscope /path/to/repo output.gif --format gif

# Custom resolution and FPS
git-chronoscope /path/to/repo output.mp4 --resolution 720p --fps 5

# Filter by branch
git-chronoscope /path/to/repo output.mp4 --branch main

# Author highlighting
git-chronoscope /path/to/repo output.mp4 --author-colors

# Include only specific files
git-chronoscope /path/to/repo output.mp4 --include "*.py" --include "*.js"

# Dry run (preview without generating)
git-chronoscope /path/to/repo output.mp4 --dry-run
```

## Programmatic API

```javascript
const { generate, checkInstallation, version } = require('git-chronoscope');

// Check if dependencies are installed
const { ok, errors } = await checkInstallation();
if (!ok) {
  console.error('Missing dependencies:', errors);
  process.exit(1);
}

// Generate a time-lapse
const result = await generate('/path/to/repo', 'output.mp4', {
  format: 'mp4',
  resolution: '1080p',
  fps: 2,
  authorColors: true,
  include: ['src/**/*.js'],
  exclude: ['node_modules/**']
});

if (result.success) {
  console.log('Video generated successfully!');
  console.log(result.output);
} else {
  console.error('Generation failed:', result.error);
}

// Get wrapper version
console.log('Version:', version());
```

## API Reference

### `generate(repoPath, outputPath, options?)`

Generate a time-lapse visualization.

**Parameters:**
- `repoPath` (string) - Path to the Git repository
- `outputPath` (string) - Path for the output file
- `options` (object, optional):
  - `format` - Output format: `'mp4'`, `'gif'`, or `'html'`
  - `branch` - Git branch to visualize
  - `fps` - Frames per second (default: 2)
  - `resolution` - `'720p'`, `'1080p'`, or `'4k'`
  - `bgColor` - Background color (hex)
  - `textColor` - Text color (hex)
  - `include` - Array of glob patterns to include
  - `exclude` - Array of glob patterns to exclude
  - `authorColors` - Enable author color highlighting
  - `noEmail` - Hide author emails
  - `redactSecrets` - Redact sensitive data
  - `dryRun` - Preview without generating
  - `sampleRate` - Process every Nth commit
  - `maxCommits` - Limit to N commits
  - `since` - Start date (YYYY-MM-DD)
  - `until` - End date (YYYY-MM-DD)

**Returns:** `Promise<{ success: boolean, output: string, error: string }>`

### `checkInstallation()`

Check if all required dependencies are installed.

**Returns:** `Promise<{ ok: boolean, errors: string[] }>`

### `version()`

Get the npm wrapper version.

**Returns:** `string`

## TypeScript Support

TypeScript type definitions are included. Import types:

```typescript
import { generate, GenerateOptions, GenerateResult } from 'git-chronoscope';

const options: GenerateOptions = {
  format: 'mp4',
  resolution: '1080p'
};

const result: GenerateResult = await generate('/repo', 'output.mp4', options);
```

## Troubleshooting

### "Python is not installed"

Install Python 3.7+ from [python.org](https://www.python.org/downloads/) and ensure it's in your PATH.

### "git-chronoscope Python package not installed"

Install the Python package:
```bash
pip install git-chronoscope
```

### "FFmpeg is not installed"

Install FFmpeg:
- **macOS**: `brew install ffmpeg`
- **Ubuntu/Debian**: `sudo apt install ffmpeg`
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Links

- [GitHub Repository](https://github.com/southpawriter02/git-chronoscope)
- [Full Documentation](https://github.com/southpawriter02/git-chronoscope#readme)
- [PyPI Package](https://pypi.org/project/git-chronoscope/)
- [Issue Tracker](https://github.com/southpawriter02/git-chronoscope/issues)

## License

MIT
