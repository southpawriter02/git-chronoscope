"""
Sensitive Data Redaction module for git-chronoscope.
Auto-detects and redacts secrets like API keys, tokens, passwords, and private keys.
"""
import re
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class SecretRedactor:
    """
    Detects and redacts sensitive data from text content.
    Uses regex patterns to identify common secret formats.
    """
    
    # Default patterns for common secrets
    DEFAULT_PATTERNS: Dict[str, str] = {
        # API Keys and Tokens
        "aws_access_key": r"(?:AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16}",
        "aws_secret_key": r"(?i)aws[_\-]?secret[_\-]?(?:access[_\-]?)?key['\"]?\s*[:=]\s*['\"]?([A-Za-z0-9/+=]{40})",
        "github_token": r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}",
        "gitlab_token": r"glpat-[A-Za-z0-9\-_]{20,}",
        "slack_token": r"xox[baprs]-[0-9A-Za-z\-]{10,}",
        "stripe_key": r"(?:sk|pk)_(?:live|test)_[0-9a-zA-Z]{24,}",
        "generic_api_key": r"(?i)(?:api[_\-]?key|apikey|api_secret)['\"]?\s*[:=]\s*['\"]?([A-Za-z0-9\-_]{16,})",
        
        # Private Keys
        "private_key_header": r"-----BEGIN (?:RSA |DSA |EC |OPENSSH |PGP )?PRIVATE KEY-----",
        "ssh_private": r"-----BEGIN OPENSSH PRIVATE KEY-----",
        
        # Passwords and Credentials
        "password_assignment": r"(?i)(?:password|passwd|pwd|secret)['\"]?\s*[:=]\s*['\"]?([^\s'\"]{8,})",
        "basic_auth": r"(?i)(?:basic\s+)[A-Za-z0-9+/=]{20,}",
        "bearer_token": r"(?i)(?:bearer\s+)[A-Za-z0-9\-_\.]{20,}",
        
        # Connection Strings
        "db_connection": r"(?i)(?:mongodb|postgres|mysql|redis|amqp)://[^\s'\"]+:[^\s'\"]+@",
        "jdbc_connection": r"(?i)jdbc:[a-z]+://[^\s'\"]+:[^\s'\"]+@",
        
        # Other Secrets
        "jwt_token": r"eyJ[A-Za-z0-9\-_]+\.eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+",
        "ssh_key_fingerprint": r"SHA256:[A-Za-z0-9+/]{43}",
        "hex_secret": r"(?i)(?:secret|token|key)['\"]?\s*[:=]\s*['\"]?([a-f0-9]{32,})",
    }
    
    def __init__(self, enabled: bool = True):
        """
        Initialize the secret redactor.
        
        :param enabled: Whether redaction is enabled.
        """
        self.enabled = enabled
        self.patterns: Dict[str, re.Pattern] = {}
        self.redaction_count = 0
        
        if enabled:
            self._compile_default_patterns()
    
    def _compile_default_patterns(self) -> None:
        """Compile default regex patterns."""
        for name, pattern in self.DEFAULT_PATTERNS.items():
            try:
                self.patterns[name] = re.compile(pattern)
            except re.error:
                pass  # Skip invalid patterns
    
    def add_pattern(self, name: str, pattern: str) -> bool:
        """
        Add a custom redaction pattern.
        
        :param name: Name for the pattern (used in redaction placeholder).
        :param pattern: Regex pattern string.
        :return: True if pattern was added successfully.
        """
        try:
            self.patterns[name] = re.compile(pattern)
            return True
        except re.error:
            return False
    
    def redact_content(self, content: str) -> Tuple[str, int]:
        """
        Redact sensitive data from content.
        
        :param content: Text content to scan and redact.
        :return: Tuple of (redacted_content, count_of_redactions).
        """
        if not self.enabled or not content:
            return content, 0
        
        redacted = content
        count = 0
        
        for name, pattern in self.patterns.items():
            # Find all matches
            matches = pattern.findall(redacted)
            if matches:
                # Replace with redacted placeholder
                redacted = pattern.sub(f"[REDACTED:{name}]", redacted)
                count += len(matches) if isinstance(matches, list) else 1
        
        self.redaction_count += count
        return redacted, count
    
    def redact_file_tree(self, file_tree: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        """
        Redact sensitive data from all files in a file tree.
        
        :param file_tree: Dictionary mapping file paths to contents.
        :return: Tuple of (redacted_file_tree, total_redactions).
        """
        if not self.enabled:
            return file_tree, 0
        
        redacted_tree = {}
        total_count = 0
        
        for path, content in file_tree.items():
            redacted_content, count = self.redact_content(content)
            redacted_tree[path] = redacted_content
            total_count += count
        
        return redacted_tree, total_count
    
    def get_stats(self) -> Dict:
        """
        Get redaction statistics.
        
        :return: Dictionary with stats.
        """
        return {
            "enabled": self.enabled,
            "patterns_count": len(self.patterns),
            "total_redactions": self.redaction_count
        }
