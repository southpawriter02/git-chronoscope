"""
File Access Control for git-chronoscope.
Parses .agentignore files to restrict file access.
"""
import os
import fnmatch
from typing import List, Set, Optional


class AccessControl:
    """
    Controls file access based on .agentignore patterns.
    Similar to .gitignore but for restricting agent access.
    """
    
    def __init__(self, patterns: Optional[List[str]] = None):
        """
        Initialize access control with optional patterns.
        
        :param patterns: List of glob patterns to block.
        """
        self.blocked_patterns: List[str] = patterns or []
        self.negated_patterns: List[str] = []  # Patterns that start with !
        self.denied_count = 0
    
    def load_from_file(self, filepath: str) -> bool:
        """
        Load patterns from an .agentignore file.
        
        :param filepath: Path to the .agentignore file.
        :return: True if file was loaded, False otherwise.
        """
        if not os.path.exists(filepath):
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Handle negation patterns
                    if line.startswith('!'):
                        self.negated_patterns.append(line[1:])
                    else:
                        self.blocked_patterns.append(line)
            
            return True
        except (IOError, OSError):
            return False
    
    def add_pattern(self, pattern: str) -> None:
        """
        Add a single pattern to the block list.
        
        :param pattern: Glob pattern to block.
        """
        if pattern.startswith('!'):
            self.negated_patterns.append(pattern[1:])
        else:
            self.blocked_patterns.append(pattern)
    
    def is_allowed(self, file_path: str) -> bool:
        """
        Check if access to a file path is allowed.
        
        :param file_path: The file path to check.
        :return: True if allowed, False if blocked.
        """
        # Normalize the path
        normalized_path = os.path.normpath(file_path)
        
        # Check against blocked patterns
        is_blocked = False
        
        for pattern in self.blocked_patterns:
            # Handle directory patterns (ending with /)
            if pattern.endswith('/'):
                dir_pattern = pattern.rstrip('/')
                # Check if path is inside this directory
                if normalized_path.startswith(dir_pattern + os.sep) or \
                   fnmatch.fnmatch(normalized_path, dir_pattern + '/*') or \
                   fnmatch.fnmatch(os.path.dirname(normalized_path), dir_pattern):
                    is_blocked = True
                    break
            else:
                # Standard glob matching
                if fnmatch.fnmatch(normalized_path, pattern) or \
                   fnmatch.fnmatch(os.path.basename(normalized_path), pattern):
                    is_blocked = True
                    break
        
        # Check negation patterns (allow exceptions)
        if is_blocked:
            for pattern in self.negated_patterns:
                if fnmatch.fnmatch(normalized_path, pattern) or \
                   fnmatch.fnmatch(os.path.basename(normalized_path), pattern):
                    is_blocked = False
                    break
        
        if is_blocked:
            self.denied_count += 1
        
        return not is_blocked
    
    def filter_file_tree(self, file_tree: dict) -> tuple:
        """
        Filter a file tree dictionary, removing blocked files.
        
        :param file_tree: Dictionary mapping file paths to contents.
        :return: Tuple of (filtered_tree, denied_count)
        """
        filtered = {}
        denied = 0
        
        for path, content in file_tree.items():
            if self.is_allowed(path):
                filtered[path] = content
            else:
                denied += 1
        
        return filtered, denied
    
    def get_stats(self) -> dict:
        """
        Get statistics about access control.
        
        :return: Dictionary with stats.
        """
        return {
            'blocked_patterns': len(self.blocked_patterns),
            'negated_patterns': len(self.negated_patterns),
            'total_denied': self.denied_count
        }
