# Security

This document outlines the security features implemented in the Git Time-Lapse tool. The goal is to ensure that the tool operates safely and does not expose sensitive information, either from the repository being analyzed or from the user's environment.

## Implemented Features

### 1. Sensitive Data Redaction

- **Purpose:** To prevent the accidental exposure of secrets and other sensitive information.
- **Functionality:** The tool automatically scans all file content and commit metadata for patterns that match common secret formats (e.g., API keys, private keys). When a potential secret is detected, it is replaced with a non-reversible placeholder, such as `[REDACTED_SECRET]`.
- **Current Patterns:**
  - AWS Access Keys
  - GitHub Tokens
  - Private Keys (RSA, EC, PGP, OPENSSH)
  - Generic high-entropy strings that may be API keys.
- **Limitations:**
  - The redaction is based on pattern matching and may not be perfect. It can result in both false positives (flagging non-sensitive data) and false negatives (missing a secret that doesn't match a known pattern).
  - The redaction is a one-way process. The original content cannot be recovered from the redacted version.
- **Configuration:** The set of redaction patterns can be extended programmatically. Future versions may include a configuration file for easier customization.

---

*This document will be updated as more security features are implemented.*
