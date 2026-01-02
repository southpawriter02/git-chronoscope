# Linear Integration

## Implementation Status
**⏳ NOT IMPLEMENTED**

## 1. Feature Description

This feature integrates git-chronoscope with Linear, allowing users to generate time-lapses for issues and projects with Linear issue tracking.

## 2. Intended Functionality

- Filter commits by Linear issue ID (e.g., TSK-123)
- Similar to Jira integration pattern
- Link time-lapse to Linear issues via API
- Generate time-lapse showing work on a specific project
- Comment on Linear issues with video link
- Webhook trigger on issue completion

## 3. Requirements

- **Dependencies:**
    - Linear API for issue lookup
    - OAuth for Linear authentication
    - Issue ID pattern matching (`[A-Z]+-[0-9]+`)
- LinearExtractor class similar to JiraExtractor
- CLI flag: `--linear-issue TSK-123`

## 4. Limitations

- Depends on developers referencing Linear IDs in commits
- API rate limits
- Linear is less widespread than Jira
