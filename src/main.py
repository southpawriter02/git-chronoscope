import argparse
import os
import tempfile
import shutil
from src.git_utils import GitRepo
from src.frame_renderer import FrameRenderer
from src.video_encoder import VideoEncoder

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

def main():
    """
    Main function for the git-chronoscope tool.
    """
    parser = argparse.ArgumentParser(
        description="Generate a time-lapse video of a Git repository's history.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("repo_path", help="Path to the local Git repository.")
    parser.add_argument("output_path", help="Path to the output video file (e.g., 'timelapse.mp4').")
    parser.add_argument(
        "--format",
        default="mp4",
        choices=["mp4", "gif"],
        help="Output video format. Default: mp4"
    )
    parser.add_argument(
        "--branch",
        default=None,
        help="The Git branch to generate the time-lapse for. Defaults to the current active branch."
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=2,
        help="Frames per second for the output video. Default: 2"
    )
    parser.add_argument(
        "--resolution",
        default="1080p",
        choices=["720p", "1080p", "4k"],
        help="Resolution of the output video. Default: 1080p"
    )
    parser.add_argument(
        "--bg-color",
        default="#141618",
        help="Background color in hex format (e.g., '#RRGGBB'). Default: #141618"
    )
    parser.add_argument(
        "--text-color",
        default="#FFFFFF",
        help="Text color in hex format (e.g., '#RRGGBB'). Default: #FFFFFF"
    )
    parser.add_argument(
        "--font-path",
        default=None,
        help="Path to a .ttf font file. Default: Pillow's default font"
    )
    parser.add_argument(
        "--font-size",
        type=int,
        default=15,
        help="Font size for the text. Default: 15"
    )
    parser.add_argument(
        "--no-email",
        action="store_true",
        help="Do not display author emails in the video."
    )
    parser.add_argument(
        "--include",
        action="append",
        default=None,
        metavar="PATTERN",
        help="Glob pattern for files to include (can be specified multiple times). Example: '*.py' or 'src/*'"
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=None,
        metavar="PATTERN",
        help="Glob pattern for files to exclude (can be specified multiple times). Example: 'tests/*' or '*.log'"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be generated without creating the video. Shows commit count, file stats, and estimated duration."
    )
    parser.add_argument(
        "--author-colors",
        action="store_true",
        help="Enable author highlighting - each author gets a unique color in the video."
    )

    args = parser.parse_args()

    # Create a temporary directory to store frames
    temp_dir = tempfile.mkdtemp()
    print(f"Using temporary directory for frames: {temp_dir}")

    try:
        # --- 1. Initialize modules ---
        resolutions = {
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "4k": (3840, 2160)
        }
        width, height = resolutions[args.resolution]

        frame_renderer = FrameRenderer(
            width=width,
            height=height,
            bg_color=args.bg_color,
            text_color=args.text_color,
            font_path=args.font_path,
            font_size=args.font_size,
            no_email=args.no_email
        )
        git_repo = GitRepo(args.repo_path)

        # --- 2. Get Git history ---
        print(f"Analyzing repository and fetching commit history for branch '{args.branch or git_repo.repo.active_branch.name}'...")
        history = git_repo.get_commit_history(branch=args.branch)

        if not history:
            print("No commits found in the specified branch. Exiting.")
            return

        # --- 3. Filter commits based on path patterns ---
        include_patterns = args.include
        exclude_patterns = args.exclude
        
        if include_patterns or exclude_patterns:
            print(f"Applying path filters - Include: {include_patterns or 'all'}, Exclude: {exclude_patterns or 'none'}")
            # Filter history to only include commits that affect filtered paths
            filtered_history = [
                commit for commit in history
                if git_repo.commit_affects_filtered_paths(
                    commit['commit_obj'],
                    include_patterns=include_patterns,
                    exclude_patterns=exclude_patterns
                )
            ]
            skipped = len(history) - len(filtered_history)
            if skipped > 0:
                print(f"Skipped {skipped} commits that don't affect filtered paths.")
            history = filtered_history

        if not history:
            print("No commits found matching the filter criteria. Exiting.")
            return

        # --- Dry Run Mode ---
        if args.dry_run:
            print("\n" + "="*60)
            print("DRY RUN MODE - Preview of time-lapse generation")
            print("="*60)
            print(f"\n📁 Repository: {args.repo_path}")
            print(f"🌿 Branch: {args.branch or git_repo.repo.active_branch.name}")
            print(f"📊 Total commits to process: {len(history)}")
            
            # Calculate file statistics
            first_commit = history[0]
            last_commit = history[-1]
            first_tree = git_repo.get_file_tree_at_commit(first_commit['commit_obj'])
            last_tree = git_repo.get_file_tree_at_commit(last_commit['commit_obj'])
            
            if include_patterns or exclude_patterns:
                first_tree = git_repo.filter_file_tree(first_tree, include_patterns, exclude_patterns)
                last_tree = git_repo.filter_file_tree(last_tree, include_patterns, exclude_patterns)
            
            print(f"\n📈 File count progression:")
            print(f"   First commit ({first_commit['hash']}): {len(first_tree)} files")
            print(f"   Last commit ({last_commit['hash']}): {len(last_tree)} files")
            
            # Calculate estimated video duration
            duration_seconds = len(history) / args.fps
            minutes = int(duration_seconds // 60)
            seconds = int(duration_seconds % 60)
            print(f"\n⏱️  Estimated video duration: {minutes}m {seconds}s (at {args.fps} fps)")
            print(f"🎬 Output format: {args.format.upper()}")
            print(f"📐 Resolution: {args.resolution}")
            
            # Show date range
            print(f"\n📅 Date range:")
            print(f"   From: {first_commit['date'].strftime('%Y-%m-%d %H:%M')}")
            print(f"   To:   {last_commit['date'].strftime('%Y-%m-%d %H:%M')}")
            
            # Show unique authors
            authors = set(c['author_name'] for c in history)
            print(f"\n👥 Authors: {len(authors)}")
            for author in sorted(authors):
                count = sum(1 for c in history if c['author_name'] == author)
                print(f"   - {author} ({count} commits)")
            
            print("\n" + "="*60)
            print("To generate the video, run without --dry-run")
            print("="*60 + "\n")
            return

        print(f"Processing {len(history)} commits. Starting frame rendering...")

        # --- Generate author colors if enabled ---
        author_colors = None
        if args.author_colors:
            authors = set(c['author_name'] for c in history)
            author_colors = FrameRenderer.generate_author_colors(authors)
            print(f"Author highlighting enabled for {len(authors)} authors.")

        # --- 4. Render frames for each commit ---
        frame_paths = []
        frame_index = 0
        
        # Use tqdm if available, otherwise simple progress
        if HAS_TQDM:
            commit_iterator = tqdm(enumerate(history), total=len(history), desc="Rendering frames", unit="frame")
        else:
            commit_iterator = enumerate(history)
        
        for i, commit in commit_iterator:
            if not HAS_TQDM:
                progress = f"[{i+1}/{len(history)}]"
                print(f"{progress} Rendering frame for commit {commit['hash']}...")

            file_contents = git_repo.get_file_tree_at_commit(commit['commit_obj'])
            
            # Apply path filtering to file tree
            if include_patterns or exclude_patterns:
                file_contents = git_repo.filter_file_tree(
                    file_contents,
                    include_patterns=include_patterns,
                    exclude_patterns=exclude_patterns
                )
            
            # Set author color for this frame if enabled
            if author_colors:
                frame_renderer.set_author_color(author_colors.get(commit['author_name']))
            
            frame = frame_renderer.render_frame(commit, file_contents)

            frame_path = os.path.join(temp_dir, f"frame_{frame_index:05d}.png")
            frame.save(frame_path)
            frame_paths.append(frame_path)
            frame_index += 1

        # --- 4. Encode video from frames ---
        print("All frames rendered. Starting video encoding...")
        video_encoder = VideoEncoder(args.output_path, frame_rate=args.fps, format=args.format)
        video_encoder.create_video_from_frames(frame_paths)

        print(f"\nTime-lapse video successfully generated at: {args.output_path}")

    except (ValueError, FileNotFoundError, RuntimeError) as e:
        print(f"\nAn error occurred: {e}")
    finally:
        # --- 5. Cleanup ---
        print(f"Cleaning up temporary directory: {temp_dir}")
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
