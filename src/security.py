import re

class DataRedactor:
    """
    A class to redact sensitive information from text.
    """
    def __init__(self, custom_patterns=None):
        """
        Initializes the DataRedactor with a set of regex patterns for secrets.
        """
        # A dictionary of regex patterns for common secrets.
        # The keys are the names of the secret types, and the values are the regex patterns.
        self.patterns = {
            "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
            "github_token": re.compile(r"ghp_[0-9a-zA-Z]{36}"),
            "private_key": re.compile(r"-----BEGIN (RSA|EC|PGP|OPENSSH) PRIVATE KEY-----"),
            "generic_api_key": re.compile(r"[a-zA-Z0-9_]{32,64}"), # A generic pattern for long, random-looking strings.
        }

        if custom_patterns:
            # If custom patterns are provided, merge them with the default ones.
            # This allows for easy extension of the redaction capabilities.
            self.patterns.update(custom_patterns)

    def redact(self, text: str) -> str:
        """
        Redacts sensitive information from a given string.

        :param text: The input string to sanitize.
        :return: The sanitized string with secrets replaced by a placeholder.
        """
        if not isinstance(text, str):
            # If the input is not a string, return it as is.
            return text

        # Iterate over all the defined patterns and apply them to the text.
        for secret_type, pattern in self.patterns.items():
            # Replace any found secrets with a placeholder.
            # The placeholder includes the type of secret that was redacted.
            text = pattern.sub(f"[REDACTED_{secret_type.upper()}]", text)

        return text
