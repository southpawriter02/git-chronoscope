"""
Unit tests for security modules: cache, redactor, sandbox, access_control, audit.
"""
import unittest
import tempfile
import os
import shutil
from src.cache import FrameCache
from src.redactor import SecretRedactor
from src.sandbox import Sandbox
from src.access_control import AccessControl
from src.audit import AuditLogger
from src.input_sanitizer import InputSanitizer


class TestFrameCache(unittest.TestCase):
    """Tests for FrameCache class."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.cache = FrameCache(self.temp_dir, cache_dir=self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init(self):
        """Test cache initialization."""
        self.assertIsNotNone(self.cache)
        self.assertEqual(self.cache.hits, 0)
        self.assertEqual(self.cache.misses, 0)
    
    def test_get_miss(self):
        """Test cache miss returns None."""
        result = self.cache.get("abc123", {"width": 800})
        self.assertIsNone(result)
        self.assertEqual(self.cache.misses, 1)
    
    def test_get_stats(self):
        """Test cache statistics."""
        stats = self.cache.get_stats()
        self.assertEqual(stats["hits"], 0)
        self.assertEqual(stats["misses"], 0)


class TestSecretRedactor(unittest.TestCase):
    """Tests for SecretRedactor class."""
    
    def test_init_enabled(self):
        """Test enabled redactor."""
        redactor = SecretRedactor(enabled=True)
        self.assertTrue(redactor.enabled)
        self.assertGreater(len(redactor.patterns), 0)
    
    def test_init_disabled(self):
        """Test disabled redactor."""
        redactor = SecretRedactor(enabled=False)
        self.assertFalse(redactor.enabled)
    
    def test_redact_github_token(self):
        """Test GitHub token redaction."""
        redactor = SecretRedactor()
        content = "token: ghp_1234567890abcdefghijklmnopqrstuvwxyz12"
        redacted, count = redactor.redact_content(content)
        self.assertIn("[REDACTED:", redacted)
        self.assertGreater(count, 0)
    
    def test_redact_disabled(self):
        """Test no redaction when disabled."""
        redactor = SecretRedactor(enabled=False)
        content = "secret = mysecretpassword123"
        redacted, count = redactor.redact_content(content)
        self.assertEqual(content, redacted)
        self.assertEqual(count, 0)


class TestSandbox(unittest.TestCase):
    """Tests for Sandbox class."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.sandbox = Sandbox(self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init(self):
        """Test sandbox initialization."""
        self.assertIsNotNone(self.sandbox.root_path)
        self.assertEqual(len(self.sandbox.violations), 0)
    
    def test_path_within_sandbox(self):
        """Test path inside sandbox."""
        test_path = os.path.join(self.temp_dir, "test.txt")
        self.assertTrue(self.sandbox.is_within_sandbox(test_path))
    
    def test_path_outside_sandbox(self):
        """Test path outside sandbox."""
        self.assertFalse(self.sandbox.is_within_sandbox("/etc/passwd"))
    
    def test_validate_relative_path(self):
        """Test relative path validation."""
        resolved, is_valid = self.sandbox.validate_path("file.txt")
        self.assertTrue(is_valid)


class TestAccessControl(unittest.TestCase):
    """Tests for AccessControl class."""
    
    def test_init(self):
        """Test access control initialization."""
        ac = AccessControl()
        self.assertIsNotNone(ac)
    
    def test_default_blocklist(self):
        """Test default blocklist is loaded."""
        ac = AccessControl(use_defaults=True)
        self.assertGreater(len(ac.blocked_patterns), 0)
    
    def test_is_allowed(self):
        """Test file accessibility check."""
        ac = AccessControl(use_defaults=True)
        # .env files should be blocked
        self.assertFalse(ac.is_allowed(".env"))
        # Regular Python files should be accessible
        self.assertTrue(ac.is_allowed("main.py"))


class TestInputSanitizer(unittest.TestCase):
    """Tests for InputSanitizer class."""
    
    def test_init(self):
        """Test sanitizer initialization."""
        sanitizer = InputSanitizer(strict_mode=False)
        self.assertFalse(sanitizer.strict_mode)
    
    def test_sanitize_path_normal(self):
        """Test normal path sanitization."""
        sanitizer = InputSanitizer()
        path, is_valid = sanitizer.sanitize_path("src/main.py")
        self.assertTrue(is_valid)
        self.assertIn("main.py", path)
    
    def test_sanitize_path_traversal(self):
        """Test path traversal detection."""
        sanitizer = InputSanitizer(strict_mode=True)
        path, is_valid = sanitizer.sanitize_path("../../../etc/passwd")
        self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()
