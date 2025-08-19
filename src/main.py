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

        print(f"Found {len(history)} commits. Starting frame rendering...")

        # --- 3. Render frames for each commit ---
        frame_paths = []
        for i, commit in enumerate(history):
            progress = f"[{i+1}/{len(history)}]"
            print(f"{progress} Rendering frame for commit {commit['hash']}...")

            file_contents = git_repo.get_file_tree_at_commit(commit['commit_obj'])
            frame = frame_renderer.render_frame(commit, file_contents)

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
