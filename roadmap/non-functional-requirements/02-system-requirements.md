# System Requirements

## 1. Description

This document outlines the minimum and recommended system requirements for running the Git Time-Lapse tool.

## 2. Operating Systems

- The tool should be cross-platform and support the following operating systems:
    - **Windows:** Windows 10 and later.
    - **macOS:** macOS 10.15 (Catalina) and later.
    - **Linux:** Major distributions like Ubuntu, Fedora, Debian, etc.

## 3. Hardware Requirements

The hardware requirements will vary depending on the size of the repository being processed and the desired output quality.

- **Minimum Requirements:**
    - **CPU:** Dual-core processor.
    - **RAM:** 4 GB.
    - **Disk Space:** 1 GB of free disk space for the tool itself and its dependencies, plus additional space for the generated videos and cache.

- **Recommended Requirements (for large repositories or high-quality output):**
    - **CPU:** Quad-core processor or better.
    - **RAM:** 8 GB or more.
    - **Disk Space:** 10 GB or more of free disk space on a fast drive (SSD).

## 4. Software Requirements

- **Git:** Version 2.25 or later.
- **FFmpeg:** A recent version of FFmpeg.
- **Programming Language Runtime:** If the tool is implemented in a language like Python or Node.js, the corresponding runtime environment will be required. The specific version will be documented.

## 5. Docker Environment

- If the tool is distributed as a Docker container, the only requirement will be a working Docker installation on the host system. This is the recommended way to run the tool to avoid issues with dependencies and system configuration.
