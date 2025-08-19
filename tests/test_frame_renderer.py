import unittest
import tempfile
import os
from PIL import Image
from datetime import datetime
from src.frame_renderer import FrameRenderer

class TestFrameRenderer(unittest.TestCase):
    def setUp(self):
        self.width = 1920
        self.height = 1080
        self.renderer = FrameRenderer(self.width, self.height)
        self.commit_info = {
            'hash': 'a1b2c3d',
            'author_name': 'Jules',
            'author_email': 'jules@example.com',
            'date': datetime.now(),
            'message': 'Test commit message'
        }
        self.file_contents = {
            'src/main.py': 'import antigravity',
            'src/git_utils.py': '# This is a git util',
            'src/frame_renderer.py': '# Renders frames',
            'tests/test_main.py': 'import unittest',
            'tests/test_git_utils.py': 'from git import Repo',
            'tests/test_frame_renderer.py': 'from PIL import Image'
        }

    def test_render_frame(self):
        img = self.renderer.render_frame(self.commit_info, self.file_contents)

        self.assertIsInstance(img, Image.Image)
        self.assertEqual(img.size, (self.width, self.height))

        # Save the image to a temporary file to ensure it's valid
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img.save(tmp.name)
            self.assertTrue(os.path.exists(tmp.name))
            self.assertGreater(os.path.getsize(tmp.name), 0)
        os.remove(tmp.name)

if __name__ == '__main__':
    unittest.main()
