import unittest
from src.security import DataRedactor

class TestDataRedactor(unittest.TestCase):
    """
    Unit tests for the DataRedactor class.
    """

    def setUp(self):
        """
        Set up a DataRedactor instance for testing.
        """
        self.redactor = DataRedactor()

    def test_redact_aws_access_key(self):
        """
        Test that AWS access keys are redacted.
        """
        text = "My AWS access key is AKIAIOSFODNN7EXAMPLE."
        redacted_text = self.redactor.redact(text)
        self.assertIn("[REDACTED_AWS_ACCESS_KEY]", redacted_text)
        self.assertNotIn("AKIAIOSFODNN7EXAMPLE", redacted_text)

    def test_redact_github_token(self):
        """
        Test that GitHub tokens are redacted.
        """
        text = "My GitHub token is ghp_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0."
        redacted_text = self.redactor.redact(text)
        self.assertIn("[REDACTED_GITHUB_TOKEN]", redacted_text)
        self.assertNotIn("ghp_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0", redacted_text)

    def test_redact_private_key(self):
        """
        Test that private keys are redacted.
        """
        text = "-----BEGIN RSA PRIVATE KEY----- a_very_long_key -----END RSA PRIVATE KEY-----"
        redacted_text = self.redactor.redact(text)
        self.assertIn("[REDACTED_PRIVATE_KEY]", redacted_text)
        self.assertNotIn("-----BEGIN RSA PRIVATE KEY-----", redacted_text)

    def test_redact_generic_api_key(self):
        """
        Test that generic API keys (long hex strings) are redacted.
        """
        text = "My API key is 1234567890abcdef1234567890abcdef1234567890abcdef."
        redacted_text = self.redactor.redact(text)
        self.assertIn("[REDACTED_GENERIC_API_KEY]", redacted_text)
        self.assertNotIn("1234567890abcdef1234567890abcdef1234567890abcdef", redacted_text)

    def test_no_redaction_for_safe_text(self):
        """
        Test that text without any secrets is not modified.
        """
        text = "This is a perfectly safe string with no secrets."
        redacted_text = self.redactor.redact(text)
        self.assertEqual(text, redacted_text)

    def test_redaction_of_multiple_secrets(self):
        """
        Test that multiple secrets in the same string are all redacted.
        """
        text = "AWS: AKIAIOSFODNN7EXAMPLE, GitHub: ghp_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
        redacted_text = self.redactor.redact(text)
        self.assertIn("[REDACTED_AWS_ACCESS_KEY]", redacted_text)
        self.assertIn("[REDACTED_GITHUB_TOKEN]", redacted_text)

    def test_non_string_input(self):
        """
        Test that non-string input is returned unmodified.
        """
        data = {"key": "value"}
        redacted_data = self.redactor.redact(data)
        self.assertEqual(data, redacted_data)

if __name__ == "__main__":
    unittest.main()
