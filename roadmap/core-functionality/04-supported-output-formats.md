# Supported Output Formats

## 1. Feature Description

This feature allows users to choose the output format for the generated time-lapse. Different formats are suitable for different use cases, such as sharing on social media, embedding in websites, or for archival purposes.

## 2. Intended Functionality

- The tool should support a variety of common video and image formats.
- **Video Formats:**
    - MP4 (H.264) - for web and mobile.
    - WebM - for modern web browsers.
    - AVI - for desktop use.
    - GIF - for short, silent animations.
- **Image Sequence:**
    - The option to export the frames as a sequence of images (e.g., PNG, JPEG) instead of a video. This is useful for users who want to use their own video editing software.

## 3. Requirements

- **Dependencies:**
    - The video encoding library (`FFmpeg`, `OpenCV`) must support the desired output formats.
- The user should be able to specify the output format via a command-line argument (e.g., `--format mp4`).

## 4. Limitations

- The availability of certain formats may depend on the codecs installed on the user's system.
- The initial version might only support a limited set of formats (e.g., MP4 and GIF).
- Fine-tuning the encoding parameters for each format might not be exposed to the user in the beginning.
