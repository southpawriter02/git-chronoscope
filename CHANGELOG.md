# Changelog

All notable changes to git-chronoscope will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.9.0-beta.1] - 2026-01-02

First public beta release establishing distribution foundation.

### Added
- Comprehensive INSTALL.md with instructions for all installation methods
- Docker Hub publishing workflow for multi-architecture images (amd64, arm64)
- Version roadmap documentation for path to v1.0
- README badges for PyPI, Docker Hub, and license
- Docker HEALTHCHECK for container health monitoring

### Changed
- Version scheme updated to 0.9.x beta series before v1.0 release
- Updated all placeholder URLs to southpawriter02/git-chronoscope
- Synchronized dependencies across pyproject.toml, setup.py, and requirements.txt
- Homebrew formulas updated for v0.9.0-beta.1
- Improved README installation section with quick install options

### Features
- **Core Functionality**
  - Time-lapse video generation from Git repository history
  - Commit information overlay (hash, author, date, message)
  - Multiple output formats: MP4, GIF, HTML interactive timeline
  - Customizable rendering options (FPS, resolution, themes, fonts, colors)

- **Advanced Features**
  - Path filtering with `--include` and `--exclude` glob patterns
  - Branch comparison with `--compare` flag
  - Author highlighting with unique colors per contributor
  - Semantic diffing with `--show-diff` flag
  - Interactive HTML timeline with searchable navigation

- **Performance & Scalability**
  - Frame caching for faster re-renders
  - Parallel processing with configurable worker count
  - Large repository support via `--sample-rate` and `--max-commits`
  - Date range filtering with `--since` and `--until`

- **Security**
  - Sensitive data redaction (API keys, passwords, tokens)
  - Input sanitization against prompt injection
  - File access control via `.agentignore`
  - Default blocklists for sensitive files
  - Filesystem sandboxing
  - Immutable audit logging
  - Dry-run mode for previewing actions

- **Integrations**
  - GitHub Actions workflow
  - GitLab CI/CD pipeline templates
  - VS Code extension
  - Jira issue filtering

- **Distribution**
  - PyPI package (`pip install git-chronoscope`)
  - Homebrew formula (`brew install git-chronoscope`)
  - Standalone executables for Windows, macOS, Linux
  - Docker image with pre-installed dependencies

- **Web GUI**
  - Flask-based web interface
  - Interactive configuration panel
  - Job history tracking
  - Real-time progress updates
  - Preview frame generation

### Documentation
- Quick start guide
- Contributing guidelines
- Troubleshooting guide
- System requirements
- Dependencies documentation

---

## Version History

| Version | Status | Focus |
|---------|--------|-------|
| 0.9.0 | Beta | First public release |
| 0.9.x | Beta | Distribution & integrations |
| 1.0.0 | Planned | Stable release |
