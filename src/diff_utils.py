"""
Diff utilities for git-chronoscope.
Computes differences between file trees and file contents.
"""
import difflib
from typing import Dict, List, Tuple, Optional


class DiffCalculator:
    """
    Calculates differences between file trees and file contents.
    """
    
    def __init__(self):
        """Initialize the diff calculator."""
        pass
    
    def compute_tree_diff(
        self, 
        old_tree: Dict[str, str], 
        new_tree: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Compare two file trees and identify file-level changes.
        
        :param old_tree: Previous commit's file tree.
        :param new_tree: Current commit's file tree.
        :return: Dictionary mapping file paths to their status:
                 'added', 'deleted', 'modified', 'unchanged'
        """
        result = {}
        
        old_files = set(old_tree.keys())
        new_files = set(new_tree.keys())
        
        # Added files (in new but not in old)
        for f in new_files - old_files:
            result[f] = 'added'
        
        # Deleted files (in old but not in new)
        for f in old_files - new_files:
            result[f] = 'deleted'
        
        # Check for modifications in common files
        for f in old_files & new_files:
            if old_tree[f] != new_tree[f]:
                result[f] = 'modified'
            else:
                result[f] = 'unchanged'
        
        return result
    
    def compute_file_diff(
        self, 
        old_content: str, 
        new_content: str
    ) -> List[Tuple[str, str]]:
        """
        Compare two versions of a file and return line-by-line diff info.
        
        :param old_content: Previous version of the file.
        :param new_content: Current version of the file.
        :return: List of tuples (status, line_content) where status is:
                 'added', 'deleted', 'unchanged'
        """
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        
        result = []
        
        # Use difflib to compute unified diff
        diff = difflib.unified_diff(old_lines, new_lines, lineterm='')
        
        # Skip the header lines (---, +++, @@)
        diff_lines = list(diff)
        
        # Parse the diff output
        for line in diff_lines:
            if line.startswith('---') or line.startswith('+++'):
                continue
            elif line.startswith('@@'):
                continue
            elif line.startswith('+'):
                result.append(('added', line[1:].rstrip('\n')))
            elif line.startswith('-'):
                result.append(('deleted', line[1:].rstrip('\n')))
            else:
                # Context line (unchanged)
                if line.startswith(' '):
                    result.append(('unchanged', line[1:].rstrip('\n')))
        
        return result
    
    def get_changed_lines(
        self, 
        old_content: Optional[str], 
        new_content: str
    ) -> Dict[int, str]:
        """
        Get a mapping of line numbers to their change status for the new content.
        
        :param old_content: Previous file content (None if new file).
        :param new_content: Current file content.
        :return: Dictionary mapping line numbers (0-indexed) to status:
                 'added', 'modified'. Lines not in dict are unchanged.
        """
        if old_content is None:
            # All lines are new
            return {i: 'added' for i in range(len(new_content.splitlines()))}
        
        if old_content == new_content:
            return {}  # No changes
        
        old_lines = old_content.splitlines()
        new_lines = new_content.splitlines()
        
        result = {}
        
        # Use SequenceMatcher to find matching blocks
        matcher = difflib.SequenceMatcher(None, old_lines, new_lines)
        
        # Get opcodes which describe transformations
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'insert':
                # Lines j1:j2 in new are inserted
                for j in range(j1, j2):
                    result[j] = 'added'
            elif tag == 'replace':
                # Lines j1:j2 in new replace lines i1:i2 in old
                for j in range(j1, j2):
                    result[j] = 'modified'
            elif tag == 'delete':
                # Lines were deleted, mark position
                pass  # We track new lines, not old
        
        return result
    
    def get_diff_summary(
        self, 
        tree_diff: Dict[str, str]
    ) -> Dict[str, int]:
        """
        Get a summary of changes from a tree diff.
        
        :param tree_diff: Result from compute_tree_diff.
        :return: Dictionary with counts: added, deleted, modified, unchanged
        """
        summary = {'added': 0, 'deleted': 0, 'modified': 0, 'unchanged': 0}
        for status in tree_diff.values():
            summary[status] = summary.get(status, 0) + 1
        return summary
