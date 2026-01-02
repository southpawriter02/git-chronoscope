# Version Roadmap to v1.0

This document outlines the versioning strategy and release plan for git-chronoscope leading up to the official v1.0 release.

## Versioning Strategy

Git-chronoscope follows [Semantic Versioning](https://semver.org/):
- **0.9.x-beta.N**: Beta releases with new features
- **0.9.x-rc.N**: Release candidates for stabilization
- **1.0.0**: First stable production release

## Current Status

**Version**: 0.9.0 (beta)

### What's Complete
- Core time-lapse generation functionality
- All advanced visualization features
- Full security suite (12/12 features)
- Performance optimizations
- CI/CD integrations (GitHub, GitLab, VS Code, Jira)
- Distribution infrastructure (PyPI, Homebrew, executables)

### What's In Progress
- Docker Hub image publishing
- npm package wrapper

### What's Planned for v1.0
- Slack integration
- Discord bot
- Linear integration

---

## Release Schedule

### v0.9.0-beta.1 - Distribution Foundation
**Status**: In Progress

Establish core distribution channels:
- [x] PyPI package configuration
- [x] Homebrew formula
- [x] Standalone executable build scripts
- [x] Docker Hub CI workflow
- [ ] First PyPI publication
- [ ] First Docker Hub publication
- [ ] First GitHub Release with executables

### v0.9.0-beta.2 - npm Package
**Status**: Planned

JavaScript ecosystem distribution:
- [ ] Node.js CLI wrapper
- [ ] npx zero-install support
- [ ] npm registry publication

### v0.9.0-beta.3 - Slack Integration
**Status**: Planned

Team collaboration features:
- [ ] Slack bot application
- [ ] `/chronoscope` slash command
- [ ] Threaded progress updates
- [ ] Interactive configuration

### v0.9.0-beta.4 - Discord Bot
**Status**: Planned

Community distribution:
- [ ] Discord bot using discord.py
- [ ] Slash commands
- [ ] Video preview embeds

### v0.9.0-beta.5 - Linear Integration
**Status**: Planned

Issue tracking support:
- [ ] Linear API client
- [ ] `--linear-issue` CLI flag
- [ ] Webhook triggers

### v0.9.0-rc.1 - Release Candidate
**Status**: Planned

Stabilization and polish:
- [ ] Comprehensive cross-platform testing
- [ ] Documentation review
- [ ] Performance benchmarking
- [ ] Security audit
- [ ] Bug fixes from beta feedback

### v1.0.0 - Official Release
**Status**: Planned

Production-ready release criteria:
- [ ] All distribution channels published
- [ ] Slack and Discord integrations functional
- [ ] Linear integration complete
- [ ] Documentation complete
- [ ] No critical bugs
- [ ] Security review passed

---

## Post-1.0 Roadmap

Features planned for future major versions:

| Version | Features |
|---------|----------|
| v1.1 | Mobile Apps (iOS/Android), Custom Themes |
| v1.2 | Analytics Dashboard |
| v1.3 | AI-Powered Narration |
| v1.4 | Real-Time Streaming |
| v2.0 | Web Dashboard (SaaS) |

---

## Distribution Matrix

| Channel | v0.9.0 | v1.0.0 |
|---------|--------|--------|
| PyPI | ✅ | ✅ |
| Homebrew | ✅ | ✅ |
| Standalone | ✅ | ✅ |
| Docker Hub | ✅ | ✅ |
| npm | ✅ | ✅ |
| GitHub Releases | ✅ | ✅ |

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on contributing to git-chronoscope.

To help with a specific release milestone:
1. Check the release checklist above
2. Pick an unchecked item
3. Open a PR referencing the version target
