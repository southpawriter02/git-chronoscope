# git-chronoscope

A command-line tool that generates a video or animated GIF showing the evolution of a Git repository's codebase. It visualizes file creation, deletion, and code changes, creating a compelling, shareable artifact that tells the story of a project.

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

To generate a time-lapse video, run the `main.py` script with the required arguments.

### Basic Example

This command generates a 1080p MP4 video named `timelapse.mp4` from a local Git repository.

```bash
python src/main.py /path/to/your/repo timelapse.mp4
```

### Advanced Example

This command generates a 720p GIF with a frame rate of 5, using a specific branch and anonymizing author emails.

```bash
python src/main.py /path/to/your/repo output.gif --format gif --resolution 720p --fps 5 --branch feature-branch --no-email
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
