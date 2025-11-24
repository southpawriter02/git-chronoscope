# Quick Start Guide - Git Chronoscope GUI

## Overview

Git Chronoscope now includes a user-friendly web-based GUI that makes it easy to generate time-lapse videos of your Git repositories without touching the command line!

## Starting the GUI

### Step 1: Launch the Web Interface

Open your terminal and run:

```bash
cd /path/to/git-chronoscope
python launch_gui.py
```

The interface will automatically open in your default web browser at `http://127.0.0.1:5000`

### Step 2: Configure Your Time-lapse

1. **Repository Path**: Enter the full path to your Git repository
   - Example: `/home/user/projects/my-project`
   - Must be a valid Git repository

2. **Load Branches** (Optional): Click to see all available branches
   - Select a specific branch to visualize
   - Leave as "Current branch" to use the active branch

3. **Output Format**: Choose between MP4 (video) or GIF (animation)
   - MP4: Better quality, smaller file size
   - GIF: Easy to share, works everywhere

4. **Resolution**: Select the video quality
   - 720p: Smaller files, faster generation
   - 1080p: Balanced quality (recommended)
   - 4K: Highest quality, larger files

5. **Frame Rate (FPS)**: Control the speed
   - Lower (1-2): Slow, detailed visualization
   - Higher (5-10): Faster playback

6. **Colors**: Customize the appearance
   - Background Color: The canvas color
   - Text Color: Color of commit info and code
   - Font Size: Adjust readability

7. **Hide Email**: Check to anonymize author emails

### Step 3: Generate

Click the **"Generate Time-lapse"** button and watch the progress bar!

- Real-time updates show current progress
- Generation time depends on repository size
- Small repos: 30 seconds - 2 minutes
- Large repos: 5-15 minutes

### Step 4: Download

Once complete, click **"Download Time-lapse"** to save your video!

## Tips for Best Results

### Resolution Recommendations

- **For sharing online**: Use 720p or 1080p
- **For presentations**: Use 1080p or 4K
- **For social media**: Use 720p with GIF format

### Frame Rate Tips

- **Documentation/Tutorial**: 2-5 FPS (slower, readable)
- **Quick overview**: 10-15 FPS (faster)
- **Promotional video**: 5-10 FPS (balanced)

### Performance Tips

1. **Large Repositories**: 
   - Use lower resolution (720p) for faster generation
   - Consider filtering to a specific branch
   - Close other applications during generation

2. **Color Choices**:
   - Dark background + light text (default) works best
   - High contrast improves readability
   - Match your project's branding colors

3. **File Sizes**:
   - MP4 files are typically 1-10 MB
   - GIF files can be 10-50 MB for same content
   - 4K resolution significantly increases file size

## Troubleshooting

### "Invalid repository path" error
- Ensure the path points to a Git repository root
- Check that the path exists on your local machine
- Use absolute paths (full path from root)

### Generation takes too long
- Try lower resolution (720p)
- Use a specific branch with fewer commits
- Ensure FFmpeg is properly installed

### Browser doesn't open automatically
- Manually open: `http://127.0.0.1:5000`
- Check if another application is using port 5000
- Try restarting the launcher

### FFmpeg not found
- Install FFmpeg: https://ffmpeg.org/download.html
- Ensure FFmpeg is in your system PATH
- Restart your terminal after installation

## Advanced Usage

### Using Custom Fonts

The web GUI currently uses default fonts. To use custom fonts with the CLI:

```bash
python -m src.main /path/to/repo output.mp4 --font-path /path/to/font.ttf
```

### Batch Processing

For multiple repositories, use the CLI in a script:

```bash
for repo in /path/to/repos/*; do
    python -m src.main "$repo" "$(basename $repo).mp4"
done
```

## Support

For issues, feature requests, or questions:
- GitHub Issues: https://github.com/southpawriter02/git-chronoscope/issues
- Documentation: See README.md for full CLI documentation

## What's Next?

Check out the roadmap for upcoming features:
- Interactive timeline viewer
- VS Code extension
- GitHub Actions integration
- More export formats

Enjoy visualizing your code's evolution! 🎬
