"""
GitLab CI/CD Integration for git-chronoscope.
Provides API wrapper and CI/CD utilities.
"""
import os
import json
import logging
from typing import Optional, Dict, Any
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console handler if no handlers exist
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(handler)


class GitLabClient:
    """
    GitLab API client for CI/CD integration.
    """
    
    def __init__(self, base_url: str = None, token: str = None):
        """
        Initialize GitLab client.
        
        :param base_url: GitLab instance URL (default: from CI_SERVER_URL env var)
        :param token: API token (default: from CI_JOB_TOKEN or GITLAB_TOKEN env var)
        """
        self.base_url = base_url or os.environ.get('CI_SERVER_URL', 'https://gitlab.com')
        self.token = token or os.environ.get('GITLAB_TOKEN') or os.environ.get('CI_JOB_TOKEN')
        self.api_url = f"{self.base_url.rstrip('/')}/api/v4"
        
        logger.info(f"GitLab client initialized for {self.base_url}")
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make an API request.
        
        :param method: HTTP method
        :param endpoint: API endpoint
        :param data: Request data
        :return: Response data
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        headers = {'Content-Type': 'application/json'}
        
        if self.token:
            headers['PRIVATE-TOKEN'] = self.token
        
        logger.debug(f"Making {method} request to {url}")
        
        try:
            body = json.dumps(data).encode() if data else None
            req = Request(url, data=body, headers=headers, method=method)
            
            with urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode())
                logger.debug(f"Request successful: {response.status}")
                return result
                
        except HTTPError as e:
            logger.error(f"HTTP error: {e.code} - {e.reason}")
            raise
        except URLError as e:
            logger.error(f"URL error: {e.reason}")
            raise
    
    def get_project(self, project_id: str) -> Dict[str, Any]:
        """
        Get project information.
        
        :param project_id: Project ID or path
        :return: Project data
        """
        logger.info(f"Getting project: {project_id}")
        return self._make_request('GET', f'/projects/{project_id}')
    
    def create_merge_request_note(self, project_id: str, mr_iid: int, body: str) -> Dict[str, Any]:
        """
        Add a comment to a merge request.
        
        :param project_id: Project ID
        :param mr_iid: Merge request IID
        :param body: Comment body
        :return: Note data
        """
        logger.info(f"Adding note to MR !{mr_iid}")
        return self._make_request(
            'POST',
            f'/projects/{project_id}/merge_requests/{mr_iid}/notes',
            {'body': body}
        )
    
    @staticmethod
    def get_ci_environment() -> Dict[str, str]:
        """
        Get CI/CD environment variables.
        
        :return: Dictionary of CI variables
        """
        ci_vars = {
            'project_id': os.environ.get('CI_PROJECT_ID', ''),
            'project_path': os.environ.get('CI_PROJECT_PATH', ''),
            'commit_sha': os.environ.get('CI_COMMIT_SHA', ''),
            'commit_branch': os.environ.get('CI_COMMIT_BRANCH', ''),
            'merge_request_iid': os.environ.get('CI_MERGE_REQUEST_IID', ''),
            'pipeline_id': os.environ.get('CI_PIPELINE_ID', ''),
            'job_id': os.environ.get('CI_JOB_ID', ''),
        }
        logger.debug(f"CI environment: {ci_vars}")
        return ci_vars
    
    @staticmethod
    def is_ci_environment() -> bool:
        """Check if running in GitLab CI."""
        return os.environ.get('GITLAB_CI', '').lower() == 'true'


def generate_artifact_link(job_name: str, artifact_path: str) -> str:
    """
    Generate a link to a job artifact.
    
    :param job_name: Name of the CI job
    :param artifact_path: Path to artifact within job
    :return: Artifact URL
    """
    project_path = os.environ.get('CI_PROJECT_PATH', '')
    job_id = os.environ.get('CI_JOB_ID', '')
    base_url = os.environ.get('CI_SERVER_URL', 'https://gitlab.com')
    
    url = f"{base_url}/{project_path}/-/jobs/{job_id}/artifacts/file/{artifact_path}"
    logger.info(f"Generated artifact link: {url}")
    return url
