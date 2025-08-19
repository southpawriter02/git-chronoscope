import subprocess
import shutil
import tempfile
import os

class VideoEncoder:
    """
    A class to encode a sequence of frames into a video file using FFmpeg.
    """
    def __init__(self, output_path, frame_rate=10, format='mp4'):
        """
        Initializes the VideoEncoder object.

        :param output_path: The path to the output video file.
        :param frame_rate: The frame rate of the video.
        :param format: The format of the video ('mp4', 'gif', etc.).
        """
        if not self.is_ffmpeg_installed():
            raise RuntimeError("FFmpeg is not installed or not found in the system's PATH. Please install it to use this feature.")

        self.output_path = output_path
        self.frame_rate = frame_rate
        self.format = format.lower()

    @staticmethod
    def is_ffmpeg_installed():
        """
        Checks if FFmpeg is installed and accessible.
        :return: True if FFmpeg is installed, False otherwise.
        """
        return shutil.which("ffmpeg") is not None

    def create_video_from_frames(self, frame_paths):
        """
        Creates a video from a sequence of frame images.

        :param frame_paths: A list of paths to the frame images.
        """
        if not frame_paths:
            print("Warning: No frames provided to create video.")
            return

        # Using a temporary file to list the input frames is safer for many files
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as tmpfile:
            for frame_path in frame_paths:
                # Path needs to be absolute and properly escaped for ffmpeg
                tmpfile.write(f"file '{os.path.abspath(frame_path)}'\n")
            list_filepath = tmpfile.name

        print(f"Generating video: {self.output_path}")

        command = self._build_ffmpeg_command(list_filepath)

        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            if result.stdout:
                print("FFmpeg output:\n", result.stdout)
            if result.stderr:
                print("FFmpeg info/warnings:\n", result.stderr)
            print(f"Video created successfully: {self.output_path}")
        except FileNotFoundError:
            raise RuntimeError("FFmpeg is not installed or not found in the system's PATH.")
        except subprocess.CalledProcessError as e:
            print("Error during video encoding with FFmpeg.")
            print(f"Command: {' '.join(command)}")
            print("FFmpeg stdout:\n", e.stdout)
            print("FFmpeg stderr:\n", e.stderr)
            raise RuntimeError("FFmpeg failed to encode the video.")
        finally:
            os.remove(list_filepath)

    def _build_ffmpeg_command(self, list_filepath):
        """
        Builds the FFmpeg command based on the specified format.
        """
        if self.format == 'mp4':
            return [
                'ffmpeg',
                '-y',  # Overwrite output file if it exists
                '-r', str(self.frame_rate),
                '-f', 'concat',
                '-safe', '0',
                '-i', list_filepath,
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p', # For compatibility
                '-preset', 'medium',
                self.output_path,
            ]
        elif self.format == 'gif':
            # Two-pass encoding for better quality GIF
            # For now, a simpler one-pass command is implemented.
            return [
                'ffmpeg',
                '-y',
                '-r', str(self.frame_rate),
                '-f', 'concat',
                '-safe', '0',
                '-i', list_filepath,
                '-filter_complex', '[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse',
                self.output_path,
            ]
        else:
            raise ValueError(f"Unsupported video format: '{self.format}'")
