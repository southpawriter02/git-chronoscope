import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
import shutil
from PIL import Image
from src.video_encoder import VideoEncoder

# This check is to make the test suite runnable in environments where ffmpeg is not installed.
# The actual check is inside the VideoEncoder class itself.
FFMPEG_INSTALLED = shutil.which("ffmpeg") is not None

class TestVideoEncoder(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.frame_paths = []
        for i in range(3):
            img = Image.new('RGB', (100, 100), color = (i * 50, i * 50, i * 50))
            path = os.path.join(self.test_dir, f'frame_{i:03d}.png')
            img.save(path)
            self.frame_paths.append(path)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch('shutil.which')
    def test_is_ffmpeg_installed(self, mock_which):
        mock_which.return_value = '/usr/bin/ffmpeg'
        self.assertTrue(VideoEncoder.is_ffmpeg_installed())

        mock_which.return_value = None
        self.assertFalse(VideoEncoder.is_ffmpeg_installed())

    @patch('src.video_encoder.VideoEncoder.is_ffmpeg_installed', return_value=False)
    def test_init_ffmpeg_not_installed(self, mock_is_installed):
        with self.assertRaisesRegex(RuntimeError, "FFmpeg is not installed"):
            VideoEncoder('output.mp4')

    @unittest.skipUnless(FFMPEG_INSTALLED, "FFmpeg is not installed, skipping FFmpeg-dependent tests.")
    def test_build_ffmpeg_command_mp4(self):
        output_path = os.path.join(self.test_dir, 'output.mp4')
        encoder = VideoEncoder(output_path, frame_rate=15, format='mp4')
        command = encoder._build_ffmpeg_command('list.txt')
        self.assertIn('libx264', command)
        self.assertIn(output_path, command)
        self.assertIn('15', command)

    @unittest.skipUnless(FFMPEG_INSTALLED, "FFmpeg is not installed, skipping FFmpeg-dependent tests.")
    def test_build_ffmpeg_command_gif(self):
        output_path = os.path.join(self.test_dir, 'output.gif')
        encoder = VideoEncoder(output_path, frame_rate=10, format='gif')
        command = encoder._build_ffmpeg_command('list.txt')
        self.assertIn('palettegen', command[-2]) # filter_complex is the second to last element
        self.assertIn(output_path, command)
        self.assertIn('10', command)

    @patch('subprocess.run')
    @patch('src.video_encoder.VideoEncoder.is_ffmpeg_installed', return_value=True)
    def test_create_video_from_frames_mocked(self, mock_is_installed, mock_run):
        output_path = os.path.join(self.test_dir, 'output.mp4')
        encoder = VideoEncoder(output_path, format='mp4')

        mock_result = MagicMock()
        mock_result.stdout = "ffmpeg output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        encoder.create_video_from_frames(self.frame_paths)

        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        command = args[0]
        self.assertEqual(command[-1], output_path)

    @unittest.skipUnless(FFMPEG_INSTALLED, "FFmpeg is not installed, skipping FFmpeg-dependent tests.")
    def test_create_video_integration(self):
        output_path = os.path.join(self.test_dir, 'output.mp4')
        encoder = VideoEncoder(output_path, frame_rate=1, format='mp4')

        encoder.create_video_from_frames(self.frame_paths)

        self.assertTrue(os.path.exists(output_path))
        self.assertGreater(os.path.getsize(output_path), 0)

if __name__ == '__main__':
    unittest.main()
