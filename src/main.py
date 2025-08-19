import argparse
import os
import tempfile
import shutil
from src.git_utils import GitRepo
from src.frame_renderer import FrameRenderer
from src.video_encoder import VideoEncoder

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

    args = parser.parse_args()

    # Create a temporary directory to store frames
    temp_dir = tempfile.mkdtemp()
    print(f"Using temporary directory for frames: {temp_dir}")

    try:
        # --- 1. Initialize modules ---
        frame_renderer = FrameRenderer(width=1920, height=1080)
        git_repo = GitRepo(args.repo_path)

        # --- 2. Get Git history ---
        print(f"Analyzing repository and fetching commit history for branch '{args.branch or git_repo.repo.active_branch.name}'...")
        history = git_repo.get_commit_history(branch=args.branch)

        if not history:
            print("No commits found in the specified branch. Exiting.")
            return

        print(f"Found {len(history)} commits. Starting frame rendering...")

        # --- 3. Render frames for each commit ---
        frame_paths = []
        for i, commit in enumerate(history):
            progress = f"[{i+1}/{len(history)}]"
            print(f"{progress} Rendering frame for commit {commit['hash']}...")

            file_tree = git_repo.get_file_tree_at_commit(commit['commit_obj'])
            frame = frame_renderer.render_frame(commit, file_tree)

            frame_path = os.path.join(temp_dir, f"frame_{i:05d}.png")
            frame.save(frame_path)
            frame_paths.append(frame_path)

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
