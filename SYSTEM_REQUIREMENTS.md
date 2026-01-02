# System Requirements

Minimum and recommended system requirements for git-chronoscope.

## Operating Systems

| OS | Version |
|----|---------|
| Windows | 10 or later |
| macOS | 10.15 (Catalina) or later |
| Linux | Ubuntu 18.04+, Fedora, Debian |

## Hardware Requirements

### Minimum
| Component | Requirement |
|-----------|-------------|
| CPU | Dual-core processor |
| RAM | 4 GB |
| Disk | 1 GB free (+ output space) |

### Recommended (large repos)
| Component | Requirement |
|-----------|-------------|
| CPU | Quad-core or better |
| RAM | 8 GB+ |
| Disk | 10 GB+ on SSD |

## Software Requirements

| Software | Version |
|----------|---------|
| Python | 3.7+ |
| Git | 2.25+ |
| FFmpeg | Latest |

## Docker Alternative

```bash
docker run -v /path/to/repo:/repo git-chronoscope /repo output.mp4
```

Using Docker eliminates all system requirements except Docker itself.
