import unittest
import json
import os
import sys
import time
import shutil
import tempfile
from unittest.mock import MagicMock, patch

# Add parent directory to path so we can import src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock modules before importing app
sys.modules['src.git_utils'] = MagicMock()
sys.modules['src.frame_renderer'] = MagicMock()
sys.modules['src.video_encoder'] = MagicMock()

# Import the app after mocking
from src.web_app import app, jobs, TimelapseJob

class WebAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Reset jobs
        jobs.clear()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Git Chronoscope', response.data)

    def test_get_branches_invalid_path(self):
        with patch('os.path.exists', return_value=False):
            response = self.app.post('/api/branches', json={'repo_path': '/invalid/path'})
            self.assertEqual(response.status_code, 400)

    def test_generate_custom_resolution(self):
        with patch('os.path.exists', return_value=True):
            # Mock threading to run synchronously or just mock it out
            with patch('threading.Thread'):
                response = self.app.post('/api/generate', json={
                    'repo_path': '/valid/path',
                    'resolution': 'custom',
                    'width': 800,
                    'height': 600
                })
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                self.assertIn('job_id', data)

                # Check if job was created with correct options
                job_id = data['job_id']
                job = jobs[job_id]
                self.assertEqual(job.options['width'], 800)
                self.assertEqual(job.options['height'], 600)

    def test_generate_invalid_custom_resolution(self):
        with patch('os.path.exists', return_value=True):
            response = self.app.post('/api/generate', json={
                'repo_path': '/valid/path',
                'resolution': 'custom',
                'width': 'invalid',
                'height': 600
            })
            self.assertEqual(response.status_code, 400)

    def test_get_jobs(self):
        # Create a dummy job
        job = TimelapseJob('test_job', '/path', {'format': 'mp4'})
        jobs['test_job'] = job

        response = self.app.get('/api/jobs')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['jobs']), 1)
        self.assertEqual(data['jobs'][0]['id'], 'test_job')

    @patch('src.web_app.GitRepo')
    @patch('src.web_app.FrameRenderer')
    def test_preview_endpoint(self, MockFrameRenderer, MockGitRepo):
        with patch('os.path.exists', return_value=True):
            # Mock GitRepo and history
            mock_repo = MockGitRepo.return_value
            mock_repo.get_commit_history.return_value = [{'commit_obj': 'mock_obj'}]
            mock_repo.get_file_tree_at_commit.return_value = {}

            # Mock FrameRenderer and render_frame
            mock_renderer = MockFrameRenderer.return_value
            mock_image = MagicMock()
            # Mock save to write to BytesIO
            def mock_save(fp, format):
                fp.write(b'fake_image_data')
            mock_image.save.side_effect = mock_save
            mock_renderer.render_frame.return_value = mock_image

            response = self.app.post('/api/preview', json={
                'repo_path': '/valid/path',
                'resolution': '1080p'
            })

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('image', data)
            # base64 of 'fake_image_data'
            # b'fake_image_data' -> ZmFrZV9pbWFnZV9kYXRh
            self.assertEqual(data['image'], 'ZmFrZV9pbWFnZV9kYXRh')

if __name__ == '__main__':
    import sys
    # Adding src to path so we can import modules for mocking
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    unittest.main()
