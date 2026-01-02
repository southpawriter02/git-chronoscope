import argparse
import os
import tempfile
import shutil
import multiprocessing
from functools import partial
from src.git_utils import GitRepo
from src.frame_renderer import FrameRenderer
from src.video_encoder import VideoEncoder
from src.cache import FrameCache
from src.timeline_generator import TimelineGenerator
from src.redactor import SecretRedactor
from src.diff_utils import DiffCalculator

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


def render_frame_worker(args):
    """
    Worker function for parallel frame rendering.
    Designed to be picklable for multiprocessing.
    
    :param args: Tuple of (index, commit_data, config)
    :return: Tuple of (index, frame_path, success)
    """
    index, commit_data, config = args
    
    try:
        # Re-initialize components in worker process
        git_repo = GitRepo(config['repo_path'])
        
        renderer = FrameRenderer(
            width=config['width'],
            height=config['height'],
            bg_color=config['bg_color'],
            text_color=config['text_color'],
            font_path=config['font_path'],
            font_size=config['font_size'],
            no_email=config['no_email']
        )
        
        redactor = SecretRedactor(enabled=config['redact_secrets'])
        
        # Get commit object by hash
        commit_obj = git_repo.repo.commit(commit_data['hash'])
        
        # Get file tree
        file_contents = git_repo.get_file_tree_at_commit(commit_obj)
        
        # Apply path filtering
        if config['include_patterns'] or config['exclude_patterns']:
            file_contents = git_repo.filter_file_tree(
                file_contents,
                include_patterns=config['include_patterns'],
                exclude_patterns=config['exclude_patterns']
            )
        
        # Apply redaction
        if redactor.enabled:
            file_contents, _ = redactor.redact_file_tree(file_contents)
        
        # Set author color
        if config['author_colors']:
            author_color = config['author_colors'].get(commit_data['author_name'])
            renderer.set_author_color(author_color)
        
        # Render frame
        frame = renderer.render_frame(commit_data, file_contents)
        
        # Save frame
        frame_path = config['frame_path_template'].format(index=index)
        frame.save(frame_path)
        
        return (index, frame_path, True)
    except Exception as e:
        return (index, str(e), False)

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
        choices=["mp4", "gif", "html"],
        help="Output format. 'mp4'/'gif' for video, 'html' for interactive timeline. Default: mp4"
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
    parser.add_argument(
        "--cache-dir",
        default=None,
        help="Custom directory for frame cache. Default: ~/.git-chronoscope/cache"
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable frame caching (always re-render all frames)."
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear cached frames for this repository before generating."
    )
    parser.add_argument(
        "--redact-secrets",
        action="store_true",
        help="Auto-detect and redact sensitive data (API keys, tokens, passwords, private keys)."
    )
    parser.add_argument(
        "--redact-pattern",
        action="append",
        default=None,
        metavar="REGEX",
        help="Custom regex pattern for redaction (can be specified multiple times)."
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Number of parallel workers for frame rendering. Default: number of CPU cores."
    )
    parser.add_argument(
        "--compare",
        metavar="BRANCH",
        default=None,
        help="Compare the main branch with another branch side-by-side."
    )
    parser.add_argument(
        "--show-diff",
        action="store_true",
        help="Highlight code changes between commits (green=added, yellow=modified)."
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

        # --- Initialize secret redactor ---
        redactor = SecretRedactor(enabled=args.redact_secrets or args.redact_pattern)
        if args.redact_pattern:
            for pattern in args.redact_pattern:
                redactor.add_pattern(f"custom_{len(redactor.patterns)}", pattern)
        if redactor.enabled:
            print(f"Secret redaction enabled with {len(redactor.patterns)} patterns.")

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

        # --- Branch Comparison Mode ---
        if args.compare:
            left_branch = args.branch or git_repo.repo.active_branch.name
            right_branch = args.compare
            
            print(f"Comparing branches: '{left_branch}' vs '{right_branch}'")
            
            # Get history for both branches
            left_history = git_repo.get_commit_history(branch=left_branch)
            right_history = git_repo.get_commit_history(branch=right_branch)
            
            if not left_history:
                print(f"No commits found in branch '{left_branch}'. Exiting.")
                return
            if not right_history:
                print(f"No commits found in branch '{right_branch}'. Exiting.")
                return
            
            print(f"Left branch ({left_branch}): {len(left_history)} commits")
            print(f"Right branch ({right_branch}): {len(right_history)} commits")
            
            # Align commits by timestamp - create unified timeline
            all_timestamps = set()
            for c in left_history:
                all_timestamps.add(c['date'])
            for c in right_history:
                all_timestamps.add(c['date'])
            
            sorted_timestamps = sorted(all_timestamps)
            
            # Create lookup by timestamp for each branch
            left_by_time = {}
            right_by_time = {}
            
            # Fill in the latest commit at or before each timestamp
            left_current = None
            for c in sorted(left_history, key=lambda x: x['date']):
                left_by_time[c['date']] = c
                left_current = c
            
            right_current = None
            for c in sorted(right_history, key=lambda x: x['date']):
                right_by_time[c['date']] = c
                right_current = c
            
            # Generate frames for comparison
            frame_paths = []
            print(f"Rendering {len(sorted_timestamps)} comparison frames...")
            
            if HAS_TQDM:
                timestamp_iterator = tqdm(enumerate(sorted_timestamps), total=len(sorted_timestamps), desc="Rendering comparison", unit="frame")
            else:
                timestamp_iterator = enumerate(sorted_timestamps)
            
            # Track current state for each branch
            left_state = None
            right_state = None
            
            for i, ts in timestamp_iterator:
                # Update state if there's a commit at this timestamp
                if ts in left_by_time:
                    left_state = left_by_time[ts]
                if ts in right_by_time:
                    right_state = right_by_time[ts]
                
                # Get file trees
                left_files = {}
                right_files = {}
                
                if left_state:
                    left_files = git_repo.get_file_tree_at_commit(left_state['commit_obj'])
                    if include_patterns or exclude_patterns:
                        left_files = git_repo.filter_file_tree(left_files, include_patterns, exclude_patterns)
                    if redactor.enabled:
                        left_files, _ = redactor.redact_file_tree(left_files)
                
                if right_state:
                    right_files = git_repo.get_file_tree_at_commit(right_state['commit_obj'])
                    if include_patterns or exclude_patterns:
                        right_files = git_repo.filter_file_tree(right_files, include_patterns, exclude_patterns)
                    if redactor.enabled:
                        right_files, _ = redactor.redact_file_tree(right_files)
                
                # Render comparison frame
                frame = frame_renderer.render_comparison_frame(
                    left_state, right_state,
                    left_files, right_files,
                    left_branch, right_branch
                )
                
                frame_path = os.path.join(temp_dir, f"frame_{i:05d}.png")
                frame.save(frame_path)
                frame_paths.append(frame_path)
            
            # Encode video
            print("All comparison frames rendered. Starting video encoding...")
            video_encoder = VideoEncoder(args.output_path, frame_rate=args.fps, format=args.format)
            video_encoder.create_video_from_frames(frame_paths)
            print(f"\nBranch comparison video generated at: {args.output_path}")
            return

        # --- HTML Interactive Timeline Generation ---
        if args.format == "html":
            print(f"Generating interactive timeline with {len(history)} commits...")
            
            # Collect file trees for each commit
            file_trees = []
            if HAS_TQDM:
                commit_iterator = tqdm(history, desc="Extracting file trees", unit="commit")
            else:
                commit_iterator = history
            
            for commit in commit_iterator:
                file_contents = git_repo.get_file_tree_at_commit(commit['commit_obj'])
                
                # Apply path filtering
                if include_patterns or exclude_patterns:
                    file_contents = git_repo.filter_file_tree(
                        file_contents,
                        include_patterns=include_patterns,
                        exclude_patterns=exclude_patterns
                    )
                
                # Apply secret redaction
                if redactor.enabled:
                    file_contents, _ = redactor.redact_file_tree(file_contents)
                
                file_trees.append(file_contents)
            
            # Generate the HTML timeline
            repo_name = os.path.basename(os.path.abspath(args.repo_path))
            branch_name = args.branch or git_repo.repo.active_branch.name
            
            timeline_gen = TimelineGenerator(repo_name, branch_name)
            timeline_gen.generate(
                commits=history,
                file_trees=file_trees,
                output_path=args.output_path,
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns
            )
            
            print(f"\nInteractive timeline generated at: {args.output_path}")
            print("Open this file in a web browser to explore your repository history!")
            return

        print(f"Processing {len(history)} commits. Starting frame rendering...")

        # --- Generate author colors if enabled ---
        author_colors = None
        if args.author_colors:
            authors = set(c['author_name'] for c in history)
            author_colors = FrameRenderer.generate_author_colors(authors)
            print(f"Author highlighting enabled for {len(authors)} authors.")

        # --- Initialize cache ---
        frame_cache = None
        cache_config = None
        if not args.no_cache:
            frame_cache = FrameCache(args.repo_path, cache_dir=args.cache_dir)
            
            # Clear cache if requested
            if args.clear_cache:
                cleared = frame_cache.clear()
                print(f"Cleared {cleared} cached frames.")
            
            # Create config hash for cache key (everything that affects frame appearance)
            cache_config = {
                'resolution': args.resolution,
                'bg_color': args.bg_color,
                'text_color': args.text_color,
                'font_size': args.font_size,
                'no_email': args.no_email,
                'include': args.include,
                'exclude': args.exclude,
                'author_colors': args.author_colors
            }

        # --- 4. Render frames for each commit ---
        num_workers = args.workers or multiprocessing.cpu_count()
        frame_paths = []
        
        # Prepare serializable commit data (remove non-picklable commit_obj)
        serializable_history = []
        for commit in history:
            serializable_commit = {
                'hash': commit.get('hash', ''),
                'author_name': commit.get('author_name', 'Unknown'),
                'author_email': commit.get('author_email', ''),
                'date': commit.get('date', None),
                'message': commit.get('message', '')
            }
            serializable_history.append(serializable_commit)
        
        # Worker config (all serializable data)
        resolutions = {
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "4k": (3840, 2160)
        }
        w, h = resolutions[args.resolution]
        
        worker_config = {
            'repo_path': args.repo_path,
            'width': w,
            'height': h,
            'bg_color': args.bg_color,
            'text_color': args.text_color,
            'font_path': args.font_path,
            'font_size': args.font_size,
            'no_email': args.no_email,
            'include_patterns': include_patterns,
            'exclude_patterns': exclude_patterns,
            'redact_secrets': redactor.enabled,
            'author_colors': author_colors,
            'frame_path_template': os.path.join(temp_dir, "frame_{index:05d}.png")
        }
        
        # Prepare work items
        work_items = [(i, serializable_history[i], worker_config) for i in range(len(serializable_history))]
        
        if num_workers > 1:
            # Parallel rendering
            print(f"Rendering {len(history)} frames using {num_workers} parallel workers...")
            
            with multiprocessing.Pool(processes=num_workers) as pool:
                if HAS_TQDM:
                    results = list(tqdm(
                        pool.imap(render_frame_worker, work_items),
                        total=len(work_items),
                        desc="Rendering frames",
                        unit="frame"
                    ))
                else:
                    results = []
                    for i, result in enumerate(pool.imap(render_frame_worker, work_items)):
                        print(f"[{i+1}/{len(work_items)}] Rendered frame {i}")
                        results.append(result)
            
            # Sort results by index and collect paths
            results.sort(key=lambda x: x[0])
            for idx, path, success in results:
                if success:
                    frame_paths.append(path)
                else:
                    print(f"Warning: Failed to render frame {idx}: {path}")
        else:
            # Sequential rendering (original approach)
            print(f"Rendering {len(history)} frames sequentially...")
            
            # Initialize diff calculator if needed
            diff_calculator = DiffCalculator() if args.show_diff else None
            prev_file_contents = None
            
            if HAS_TQDM:
                commit_iterator = tqdm(enumerate(history), total=len(history), desc="Rendering frames", unit="frame")
            else:
                commit_iterator = enumerate(history)
            
            for i, commit in commit_iterator:
                if not HAS_TQDM:
                    print(f"[{i+1}/{len(history)}] Rendering frame for commit {commit['hash']}...")
                
                frame_path = os.path.join(temp_dir, f"frame_{i:05d}.png")
                
                # Try to get from cache (only when not using diff mode)
                cached_frame = None
                if frame_cache and not args.show_diff:
                    cached_frame = frame_cache.get(commit['hash'], cache_config)
                
                if cached_frame:
                    cached_frame.save(frame_path)
                else:
                    file_contents = git_repo.get_file_tree_at_commit(commit['commit_obj'])
                    
                    if include_patterns or exclude_patterns:
                        file_contents = git_repo.filter_file_tree(
                            file_contents,
                            include_patterns=include_patterns,
                            exclude_patterns=exclude_patterns
                        )
                    
                    if redactor.enabled:
                        file_contents, _ = redactor.redact_file_tree(file_contents)
                    
                    if author_colors:
                        frame_renderer.set_author_color(author_colors.get(commit['author_name']))
                    
                    # Use diff rendering if enabled
                    if args.show_diff and diff_calculator:
                        # Calculate diffs from previous state
                        tree_diff = diff_calculator.compute_tree_diff(
                            prev_file_contents or {}, file_contents
                        )
                        
                        # Calculate line-level changes for modified/added files
                        line_changes = {}
                        for fpath, status in tree_diff.items():
                            if status in ('added', 'modified') and fpath in file_contents:
                                old_content = prev_file_contents.get(fpath) if prev_file_contents else None
                                line_changes[fpath] = diff_calculator.get_changed_lines(
                                    old_content, file_contents[fpath]
                                )
                        
                        frame = frame_renderer.render_diff_frame(commit, file_contents, tree_diff, line_changes)
                        prev_file_contents = file_contents.copy()
                    else:
                        frame = frame_renderer.render_frame(commit, file_contents)
                    
                    frame.save(frame_path)
                    
                    if frame_cache and not args.show_diff:
                        frame_cache.put(commit['hash'], cache_config, frame)
                
                frame_paths.append(frame_path)

        # --- 5. Encode video from frames ---
        print("All frames rendered. Starting video encoding...")
        
        # Print cache statistics
        if frame_cache:
            stats = frame_cache.get_stats()
            print(f"Cache stats: {stats['hits']} hits, {stats['misses']} misses ({stats['hit_rate']:.1f}% hit rate)")
        
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
