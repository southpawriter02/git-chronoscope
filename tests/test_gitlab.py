"""
Unit tests for GitLab CI/CD integration.
"""
import unittest
import os
from unittest.mock import patch, MagicMock
from src.gitlab_integration import GitLabClient, generate_artifact_link


class TestGitLabClient(unittest.TestCase):
    """Tests for GitLabClient class."""
    
    def test_init_default_url(self):
        """Test initialization with default URL."""
        client = GitLabClient()
        self.assertEqual(client.base_url, 'https://gitlab.com')
    
    def test_init_custom_url(self):
        """Test initialization with custom URL."""
        client = GitLabClient(base_url='https://gitlab.example.com')
        self.assertEqual(client.base_url, 'https://gitlab.example.com')
    
    @patch.dict(os.environ, {'CI_SERVER_URL': 'https://custom.gitlab.com'})
    def test_init_from_env(self):
        """Test initialization from environment variable."""
        client = GitLabClient()
        self.assertEqual(client.base_url, 'https://custom.gitlab.com')
    
    def test_api_url(self):
        """Test API URL construction."""
        client = GitLabClient(base_url='https://gitlab.com')
        self.assertEqual(client.api_url, 'https://gitlab.com/api/v4')
    
    def test_is_ci_environment_false(self):
        """Test CI environment detection when not in CI."""
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(GitLabClient.is_ci_environment())
    
    @patch.dict(os.environ, {'GITLAB_CI': 'true'})
    def test_is_ci_environment_true(self):
        """Test CI environment detection when in CI."""
        self.assertTrue(GitLabClient.is_ci_environment())
    
    @patch.dict(os.environ, {
        'CI_PROJECT_ID': '123',
        'CI_COMMIT_SHA': 'abc123',
        'CI_COMMIT_BRANCH': 'main'
    })
    def test_get_ci_environment(self):
        """Test getting CI environment variables."""
        env = GitLabClient.get_ci_environment()
        self.assertEqual(env['project_id'], '123')
        self.assertEqual(env['commit_sha'], 'abc123')
        self.assertEqual(env['commit_branch'], 'main')


class TestArtifactLink(unittest.TestCase):
    """Tests for artifact link generation."""
    
    @patch.dict(os.environ, {
        'CI_PROJECT_PATH': 'user/project',
        'CI_JOB_ID': '999',
        'CI_SERVER_URL': 'https://gitlab.com'
    })
    def test_generate_artifact_link(self):
        """Test artifact link generation."""
        link = generate_artifact_link('build', 'output/video.mp4')
        self.assertIn('user/project', link)
        self.assertIn('999', link)
        self.assertIn('output/video.mp4', link)


if __name__ == '__main__':
    unittest.main()
