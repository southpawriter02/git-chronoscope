# Limitations

Known limitations and constraints of git-chronoscope.

## Performance

| Factor | Impact |
|--------|--------|
| Large repos (10k+ commits) | Slower processing, use `--sample-rate` |
| Many files per commit | Higher memory usage |
| Large file sizes | Longer frame render time |

## Unsupported Content

- **Binary files**: Images, videos, executables ignored
- **Non-UTF8**: Files with encoding issues may be skipped

## Git History

- **Merge commits**: Follows first parent (configurable)
- **Shallow clones**: May have incomplete history
- **Submodules**: Not traversed by default

## Feature-Specific

| Feature | Limitation |
|---------|------------|
| Syntax highlighting | Depends on Pygments language support |
| Semantic diffing | Line-level only (not AST-based) |
| Author highlighting | Based on `git blame` accuracy |

## External Dependencies

| Dependency | Required For |
|------------|--------------|
| Git | All operations |
| FFmpeg | Video output (MP4, GIF) |
| Python 3.7+ | Runtime |

## Security

- Only use on **trusted repositories**
- Tool executes local git commands
- No network access required
