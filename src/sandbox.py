"""
Filesystem Sandboxing for git-chronoscope.
Constrains file access to the repository directory only.
"""
import os
from typing import Tuple, Optional


class Sandbox:
    """
    Filesystem sandbox that restricts file access to a root directory.
    Prevents path traversal attacks and access outside the sandbox.
    """
    
    def __init__(self, root_path: str):
        """
        Initialize the sandbox with a root directory.
        
        :param root_path: The absolute path to the sandbox root (repo directory).
        """
        # Resolve to absolute path and normalize
        self.root_path = os.path.realpath(os.path.abspath(root_path))
        self.violations = []
    
    def is_within_sandbox(self, path: str) -> bool:
        """
        Check if a path is within the sandbox.
        
        :param path: The path to check.
        :return: True if within sandbox, False otherwise.
        """
        try:
            # Resolve the path (follows symlinks)
            resolved = os.path.realpath(os.path.abspath(path))
            
            # Check if resolved path starts with sandbox root
            # Use os.path.commonpath to handle edge cases
            return resolved.startswith(self.root_path + os.sep) or resolved == self.root_path
        except (OSError, ValueError):
            return False
    
    def validate_path(self, path: str) -> Tuple[str, bool]:
        """
        Validate a path is within the sandbox.
        
        :param path: The path to validate.
        :return: Tuple of (resolved_path, is_valid).
        """
        if not path:
            return "", False
        
        try:
            # Handle relative paths by joining with root
            if not os.path.isabs(path):
                full_path = os.path.join(self.root_path, path)
            else:
                full_path = path
            
            # Resolve to real path (handles symlinks and ..)
            resolved = os.path.realpath(os.path.abspath(full_path))
            
            # Check if within sandbox
            if self.is_within_sandbox(resolved):
                return resolved, True
            else:
                self.violations.append(f"Path outside sandbox: {path} -> {resolved}")
                return "", False
                
        except (OSError, ValueError) as e:
            self.violations.append(f"Invalid path: {path} - {e}")
            return "", False
    
    def validate_output_path(self, output_path: str, allowed_dirs: Optional[list] = None) -> Tuple[str, bool]:
        """
        Validate an output path. Output can be outside sandbox but in allowed directories.
        
        :param output_path: The output path to validate.
        :param allowed_dirs: Optional list of additional allowed directories for output.
        :return: Tuple of (resolved_path, is_valid).
        """
        if not output_path:
            return "", False
        
        try:
            resolved = os.path.realpath(os.path.abspath(output_path))
            
            # Output within sandbox is always allowed
            if self.is_within_sandbox(resolved):
                return resolved, True
            
            # Check if output is in current working directory
            cwd = os.path.realpath(os.getcwd())
            if resolved.startswith(cwd + os.sep) or os.path.dirname(resolved) == cwd:
                return resolved, True
            
            # Check allowed directories
            if allowed_dirs:
                for allowed in allowed_dirs:
                    allowed_resolved = os.path.realpath(os.path.abspath(allowed))
                    if resolved.startswith(allowed_resolved + os.sep):
                        return resolved, True
            
            # Output in parent directory of output file is generally OK
            output_dir = os.path.dirname(resolved)
            if os.path.exists(output_dir) and os.access(output_dir, os.W_OK):
                return resolved, True
            
            self.violations.append(f"Output path not allowed: {output_path}")
            return "", False
            
        except (OSError, ValueError) as e:
            self.violations.append(f"Invalid output path: {output_path} - {e}")
            return "", False
    
    def get_violations(self) -> list:
        """Get list of sandbox violations."""
        return self.violations.copy()
    
    def get_stats(self) -> dict:
        """Get sandbox statistics."""
        return {
            'root_path': self.root_path,
            'violations': len(self.violations)
        }
