"""
Jira Integration for git-chronoscope.
Parses commit messages for Jira issue keys and filters commits.
"""
import re
from typing import List, Set, Optional


class JiraExtractor:
    """
    Extracts Jira issue keys from commit messages.
    """
    
    # Pattern matches Jira issue keys like PROJ-123, ABC-1, FOO-9999
    ISSUE_PATTERN = re.compile(r'\b([A-Z][A-Z0-9]+-[0-9]+)\b')
    
    def __init__(self):
        """Initialize the Jira extractor."""
        self.extracted_issues: Set[str] = set()
    
    def extract_issue_keys(self, message: str) -> List[str]:
        """
        Extract all Jira issue keys from a commit message.
        
        :param message: The commit message to parse.
        :return: List of Jira issue keys found.
        """
        if not message:
            return []
        
        matches = self.ISSUE_PATTERN.findall(message)
        for m in matches:
            self.extracted_issues.add(m)
        return matches
    
    def commit_matches_issue(self, message: str, issue_key: str) -> bool:
        """
        Check if a commit message references a specific Jira issue.
        
        :param message: The commit message.
        :param issue_key: The Jira issue key to look for.
        :return: True if the commit references the issue.
        """
        if not message or not issue_key:
            return False
        
        issue_key_upper = issue_key.upper()
        keys_in_message = self.extract_issue_keys(message)
        return issue_key_upper in [k.upper() for k in keys_in_message]
    
    def filter_commits_by_issue(self, commits: list, issue_key: str) -> list:
        """
        Filter a list of commits to only those referencing a specific issue.
        
        :param commits: List of commit objects (must have 'message' attribute).
        :param issue_key: The Jira issue key to filter by.
        :return: Filtered list of commits.
        """
        if not issue_key:
            return commits
        
        filtered = []
        for commit in commits:
            message = getattr(commit, 'message', str(commit))
            if self.commit_matches_issue(message, issue_key):
                filtered.append(commit)
        
        return filtered
    
    def get_all_issues(self) -> Set[str]:
        """
        Get all unique issue keys extracted so far.
        
        :return: Set of all extracted issue keys.
        """
        return self.extracted_issues.copy()
    
    def get_stats(self) -> dict:
        """Get extraction statistics."""
        return {
            'unique_issues': len(self.extracted_issues),
            'issues': list(self.extracted_issues)
        }
