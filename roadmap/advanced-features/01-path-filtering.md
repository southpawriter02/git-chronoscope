# Path Filtering

## 1. Feature Description

This feature allows users to focus the time-lapse on specific files or directories within the repository. This is useful for large repositories where visualizing the entire project is not practical or informative.

## 2. Intended Functionality

- Users can provide a list of file paths or directory paths to include or exclude from the time-lapse.
- The tool should support glob patterns for more flexible path matching (e.g., `src/**/*.js`, `!*.log`).
- When path filtering is active, the time-lapse should only show the specified files/directories. If a commit does not touch any of the filtered paths, it can be skipped in the time-lapse to make the video more concise.

## 3. Requirements

- The tool needs a mechanism to parse and apply the filtering rules.
- The Git history traversal logic needs to be adapted to check if a commit affects the filtered paths. This can be done by inspecting the diff of each commit.
- Command-line arguments or a configuration file to specify the include/exclude patterns.

## 4. Limitations

- In the initial implementation, the complexity of the supported glob patterns might be limited.
- The performance might be affected when filtering a repository with a very long history, as each commit needs to be inspected.
- The visualization of the filtered file tree might be challenging. For example, should empty directories be shown? This needs to be defined.
