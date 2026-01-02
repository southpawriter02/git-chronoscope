"""
Input Sanitizer for git-chronoscope.
Provides protection against prompt injection and malicious inputs.
"""
import os
import re
from typing import Tuple, List, Optional


class InputSanitizer:
    """
    Sanitizes and validates user inputs to prevent injection attacks.
    """
    
    # Shell metacharacters that could be dangerous
    SHELL_METACHARACTERS = [';', '|', '&', '$', '`', '>', '<', '!', '\n', '\r']
    
    # Suspicious patterns that might indicate injection attempts
    SUSPICIOUS_PATTERNS = [
        r'\.\./',                    # Path traversal
        r'\.\.\\',                   # Windows path traversal
        r'\x00',                     # Null byte injection
        r'%00',                      # URL-encoded null byte
        r'\$\{',                     # Variable expansion
        r'\$\(',                     # Command substitution
        r'`.*`',                     # Backtick command execution
        r';\s*(rm|cat|wget|curl)',   # Command chaining
        r'\|\s*(bash|sh|zsh)',       # Pipe to shell
    ]
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize the input sanitizer.
        
        :param strict_mode: If True, reject suspicious inputs. If False, just warn.
        """
        self.strict_mode = strict_mode
        self.warnings: List[str] = []
        self.blocked_count = 0
    
    def sanitize_path(self, path: str) -> Tuple[str, bool]:
        """
        Sanitize and validate a file path.
        
        :param path: The path to sanitize.
        :return: Tuple of (sanitized_path, is_valid).
        """
        if not path:
            return "", False
        
        # Check for null bytes
        if '\x00' in path or '%00' in path:
            self.warnings.append(f"Null byte detected in path: {repr(path)}")
            self.blocked_count += 1
            return "", False
        
        # Normalize the path
        normalized = os.path.normpath(path)
        
        # Get absolute path
        try:
            absolute = os.path.abspath(normalized)
        except (OSError, ValueError) as e:
            self.warnings.append(f"Invalid path: {path} - {e}")
            self.blocked_count += 1
            return "", False
        
        # Check for path traversal after normalization
        # If the normalized path goes outside expected boundaries, it might be suspicious
        if '..' in path:
            self.warnings.append(f"Path traversal pattern detected in: {path}")
            if self.strict_mode:
                self.blocked_count += 1
                return "", False
        
        return absolute, True
    
    def sanitize_pattern(self, pattern: str) -> Tuple[str, bool]:
        """
        Sanitize a glob or regex pattern.
        
        :param pattern: The pattern to sanitize.
        :return: Tuple of (sanitized_pattern, is_valid).
        """
        if not pattern:
            return "", False
        
        # Check for shell metacharacters in patterns
        dangerous_chars = [c for c in self.SHELL_METACHARACTERS if c in pattern]
        if dangerous_chars:
            self.warnings.append(f"Dangerous characters {dangerous_chars} in pattern: {pattern}")
            if self.strict_mode:
                self.blocked_count += 1
                return "", False
        
        # Check for null bytes
        if '\x00' in pattern:
            self.warnings.append(f"Null byte in pattern: {repr(pattern)}")
            self.blocked_count += 1
            return "", False
        
        return pattern, True
    
    def detect_suspicious_input(self, input_str: str) -> Tuple[bool, List[str]]:
        """
        Check for suspicious patterns in input.
        
        :param input_str: The input string to check.
        :return: Tuple of (is_suspicious, list of matched patterns).
        """
        if not input_str:
            return False, []
        
        matches = []
        for pattern in self.SUSPICIOUS_PATTERNS:
            if re.search(pattern, input_str, re.IGNORECASE):
                matches.append(pattern)
        
        if matches:
            self.warnings.append(f"Suspicious patterns detected: {matches}")
            if self.strict_mode:
                self.blocked_count += len(matches)
        
        return len(matches) > 0, matches
    
    def sanitize_branch_name(self, branch: str) -> Tuple[str, bool]:
        """
        Sanitize a Git branch name.
        
        :param branch: The branch name to sanitize.
        :return: Tuple of (sanitized_branch, is_valid).
        """
        if not branch:
            return "", False
        
        # Git branch names can't contain certain characters
        invalid_chars = [' ', '~', '^', ':', '?', '*', '[', '\\', '\x00']
        
        for char in invalid_chars:
            if char in branch:
                self.warnings.append(f"Invalid character '{repr(char)}' in branch name: {branch}")
                if self.strict_mode:
                    self.blocked_count += 1
                    return "", False
                # Remove invalid characters if not in strict mode
                branch = branch.replace(char, '')
        
        # Check for shell injection attempts
        is_suspicious, _ = self.detect_suspicious_input(branch)
        if is_suspicious and self.strict_mode:
            return "", False
        
        return branch, True
    
    def get_stats(self) -> dict:
        """
        Get sanitization statistics.
        
        :return: Dictionary with stats.
        """
        return {
            'warnings': len(self.warnings),
            'blocked': self.blocked_count,
            'strict_mode': self.strict_mode
        }
    
    def get_warnings(self) -> List[str]:
        """
        Get all warnings generated during sanitization.
        
        :return: List of warning messages.
        """
        return self.warnings.copy()
