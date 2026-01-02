# Troubleshooting

Common problems and solutions.

## FFmpeg Not Found

**Error:** `FFmpeg not found in PATH`

**Solution:**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
winget install FFmpeg.FFmpeg
```

## Git Not Found

**Error:** `git: command not found`

**Solution:** Install Git from https://git-scm.com/downloads

## No Commits Found

**Error:** `No commits found in the specified branch`

**Solutions:**
- Verify the repository path is correct
- Check if the branch exists: `git branch -a`
- Ensure repository is not a shallow clone

## Out of Memory

**Error:** Process killed or memory errors

**Solutions:**
- Use `--sample-rate 10` to skip commits
- Use `--max-commits 500` to limit commits
- Use `--include "*.py"` to filter files

## Permission Denied

**Error:** Cannot write output file

**Solution:** Check write permissions for output directory

## Slow Performance

**Solutions:**
- Use `--workers 4` for parallel processing
- Use `--sample-rate N` to skip commits
- Use `--use-cache` for repeated runs

## Still Having Issues?

Open an issue at: https://github.com/user/git-chronoscope/issues
