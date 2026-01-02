# GitLab CI/CD Integration

Generate time-lapse videos automatically in your GitLab pipelines.

## Quick Start

1. Copy `.gitlab-ci.yml.template` to your project as `.gitlab-ci.yml`
2. Commit and push to trigger the pipeline

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `CHRONOSCOPE_OUTPUT` | `timelapse.mp4` | Output file name |
| `CHRONOSCOPE_FPS` | `5` | Frames per second |
| `CHRONOSCOPE_FORMAT` | `mp4` | Output format |

## Docker Image

Build and push to your registry:

```bash
docker build -t registry.gitlab.com/yourgroup/chronoscope:latest .
docker push registry.gitlab.com/yourgroup/chronoscope:latest
```

Then use in your CI:

```yaml
generate-timelapse:
  image: registry.gitlab.com/yourgroup/chronoscope:latest
  script:
    - python -m src.main . output.mp4
```

## Merge Request Comments

To post artifact links to MRs, set `GITLAB_TOKEN` with API access in CI/CD variables.

## Artifacts

Generated videos are saved as job artifacts with 1-week expiry.
