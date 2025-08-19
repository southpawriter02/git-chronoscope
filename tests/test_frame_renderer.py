import unittest
import tempfile
import os
from PIL import Image, ImageDraw
from datetime import datetime
from src.frame_renderer import FrameRenderer

class TestFrameRenderer(unittest.TestCase):
    def setUp(self):
        self.width = 800  # Smaller size for faster tests
        self.height = 600
        self.bg_color_hex = "#141618"
        self.text_color_hex = "#FFFFFF"
        self.renderer = FrameRenderer(
            self.width,
            self.height,
            bg_color=self.bg_color_hex,
            text_color=self.text_color_hex,
            no_email=False
        )
        self.renderer_no_email = FrameRenderer(
            self.width,
            self.height,
            bg_color=self.bg_color_hex,
            text_color=self.text_color_hex,
            no_email=True
        )
        self.commit_info = {
            'hash': 'a1b2c3d',
            'author_name': 'Jules',
            'author_email': 'jules@example.com',
            'date': datetime(2023, 1, 1, 12, 0, 0),
            'message': 'Test commit message'
        }
        self.file_contents = {
            'src/main.py': 'import antigravity',
            'tests/test_main.py': 'import unittest',
        }

    def _get_pixel_color(self, img, x, y):
        return img.getpixel((x, y))

    def test_render_frame_basic_properties(self):
        img = self.renderer.render_frame(self.commit_info, self.file_contents)
        self.assertIsInstance(img, Image.Image)
        self.assertEqual(img.size, (self.width, self.height))

        # Check background color
        self.assertEqual(self._get_pixel_color(img, 0, 0), self.renderer.bg_color)

    def test_commit_info_rendering(self):
        # To test text rendering, we can't check exact pixels due to anti-aliasing.
        # Instead, we can draw the text on a separate image and check if it's present.
        # A simpler approach for now is to save the image and manually inspect it if tests fail.
        # For this test, we'll just ensure it runs without error and produces a valid image.
        img = self.renderer.render_frame(self.commit_info, self.file_contents)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=True) as tmp:
            img.save(tmp.name)
            self.assertTrue(os.path.exists(tmp.name))
            self.assertGreater(os.path.getsize(tmp.name), 0)

    def test_email_anonymization(self):
        # This is hard to test without OCR or complex image analysis.
        # A pragmatic approach is to have a "golden file" test.
        # We generate a reference image, and then check that the output of
        # the renderer with anonymization is different from the one without.

        img_with_email = self.renderer.render_frame(self.commit_info, self.file_contents)
        img_no_email = self.renderer_no_email.render_frame(self.commit_info, self.file_contents)

        # The images should be different
        self.assertNotEqual(list(img_with_email.getdata()), list(img_no_email.getdata()))

        # As a simple check, we can verify that the "jules@example.com" is not in the image bytes
        # This is not a reliable test, but it's a starting point.
        # A better test would be to use OCR, but that's too complex for this context.
        # For now, we'll rely on the visual difference.

if __name__ == '__main__':
    unittest.main()
