# Commit Information Overlay

## 1. Feature Description

This feature enhances the basic time-lapse by overlaying commit information onto each frame of the video. This provides context to the viewer, helping them understand what changes are being made and by whom.

## 2. Intended Functionality

- For each frame in the time-lapse video, the following information should be displayed:
    - Commit hash (short version).
    - Author name and email.
    - Commit date and time.
    - Commit message (the first line).
- The overlay should be customizable, allowing users to enable or disable it.
- The position, font, size, and color of the overlay text should be configurable.

## 3. Requirements

- **Dependencies:**
    - A library for image manipulation to draw text on the generated frames (e.g., `Pillow`'s `ImageDraw` module for Python).
- The tool needs to be able to extract the required commit metadata from the Git repository.

## 4. Limitations

- In the initial implementation, the customization options for the overlay might be limited.
- Long commit messages might be truncated to fit within the frame.
- The layout of the overlay information will be fixed in the initial version.
