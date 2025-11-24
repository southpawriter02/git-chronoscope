# git-chronoscope

A command-line tool and web-based GUI that generates a video or animated GIF showing the evolution of a Git repository's codebase. It visualizes file creation, deletion, and code changes, creating a compelling, shareable artifact that tells the story of a project.

## Features

- 🎬 Generate time-lapse videos (MP4) or animated GIFs of your Git repository
- 🖥️ **NEW: Web-based GUI** for easy configuration and generation
- 📊 Progress bars and real-time status updates
- 🎨 Customizable colors, resolution, and frame rates
- 🔒 Privacy option to hide author emails
- 🌿 Support for specific branches and commit filtering

## Installation

### Prerequisites

- Python 3.7+
- Git
- FFmpeg

Before you begin, ensure you have [FFmpeg](https://ffmpeg.org/download.html) installed and accessible in your system's PATH. FFmpeg is required for video encoding.

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/git-chronoscope.git
    cd git-chronoscope
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Web Interface (Recommended for Beginners)

The easiest way to use git-chronoscope is through the web interface:

```bash
python launch_gui.py
```

This will:
1. Start a local web server
2. Automatically open the interface in your browser at `http://127.0.0.1:5000`
3. Provide an intuitive form to configure and generate your time-lapse

**Features of the Web GUI:**
- Interactive configuration with live previews
- Load and select branches from your repository
- Real-time progress updates with visual progress bars
- One-click download of completed time-lapses
- No command-line experience required!

### Command-Line Interface

To generate a time-lapse video from the command line, run the `main.py` script with the required arguments.

### Basic Example

This command generates a 1080p MP4 video named `timelapse.mp4` from a local Git repository.

```bash
python -m src.main /path/to/your/repo timelapse.mp4
```

### Advanced Example

This command generates a 720p GIF with a frame rate of 5, using a specific branch and anonymizing author emails.

```bash
python -m src.main /path/to/your/repo output.gif --format gif --resolution 720p --fps 5 --branch feature-branch --no-email
```

## Configuration

You can customize the output by using the following command-line options:

| Argument | Description | Default |
| --- | --- | --- |
| `repo_path` | Path to the local Git repository. | (Required) |
| `output_path` | Path to the output video file. | (Required) |
| `--format` | Output video format. Choices: `mp4`, `gif`. | `mp4` |
| `--branch` | The Git branch to generate the time-lapse for. | Current active branch |
| `--fps` | Frames per second for the output video. | `2` |
| `--resolution` | Resolution of the output video. Choices: `720p`, `1080p`, `4k`. | `1080p` |
| `--bg-color` | Background color in hex format (e.g., `#141618`). | `#141618` |
| `--text-color` | Text color in hex format (e.g., `#FFFFFF`). | `#FFFFFF` |
| `--font-path` | Path to a `.ttf` font file. | Pillow's default font |
| `--font-size` | Font size for the text. | `15` |
| `--no-email` | Do not display author emails in the video. | `False` |

## What's New in This Version 🎉

- **Web-based GUI**: User-friendly interface for generating time-lapses without command-line knowledge
- **Progress Bars**: Visual feedback during CLI generation with tqdm
- **Better Documentation**: Comprehensive guides for both beginners and power users
- **Easy Launcher**: One-command start with `launch_gui.py`

## Future Enhancements

The project roadmap includes exciting features like:
- Interactive timeline viewer (HTML/JavaScript based)
- VS Code extension
- GitHub Actions integration
- Path filtering and branch comparison
- More export formats

See the [roadmap](roadmap/README.md) for detailed plans.

## Contributing

We welcome contributions! Whether it's:
- 🐛 Bug reports and fixes
- ✨ New features
- 📝 Documentation improvements
- 🎨 UI/UX enhancements

Please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
