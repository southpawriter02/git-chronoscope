# Limitations

## 1. Description

This document describes the known limitations and constraints of the Git Time-Lapse tool.

## 2. General Limitations

- **Performance:** The performance of the tool is highly dependent on the size of the repository (number of commits, number of files, size of files) and the hardware it is running on. Generating time-lapses for very large repositories can be a slow and resource-intensive process.
- **Binary Files:** The tool is designed to visualize text-based source code files. It does not handle binary files (e.g., images, videos, executables) in a meaningful way. Binary files will likely be ignored or displayed as raw data.
- **Complex Git Histories:** The tool might struggle with repositories that have very complex histories, such as those with many octopus merges or rewritten history. The default behavior is to follow the first parent of merge commits.

## 3. Feature-Specific Limitations

- **Syntax Highlighting:** The quality of the syntax highlighting depends on the underlying library (e.g., `Pygments`). Not all languages or language features may be perfectly supported.
- **Semantic Diffing:** This is an experimental and complex feature. It might not always produce accurate results and will have a significant performance impact. It will only be available for a limited set of programming languages.
- **Author Highlighting:** The accuracy of author highlighting depends on the output of `git blame`, which can sometimes be misleading, especially after refactoring.

## 4. External Dependencies

- The tool's functionality is dependent on external tools like `git` and `FFmpeg`. If these tools are not installed or are not in the system's PATH, the tool will not work.
- The supported video formats are limited by the codecs available in the user's `FFmpeg` installation.

## 5. Security

- The tool executes `git` commands on the local system. It should only be used on repositories from trusted sources. Running it on a malicious repository could potentially lead to security vulnerabilities. The tool itself does not introduce any new security risks beyond what is inherent in using Git.
