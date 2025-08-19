# Jira Integration

## 1. Feature Description

This feature integrates the Git Time-Lapse tool with Jira, allowing users to visualize the development progress of a Jira issue.

## 2. Intended Functionality

- A Jira plugin or a webhook-based integration.
- When a commit message references a Jira issue key (e.g., "PROJ-123"), the tool can associate that commit with the corresponding issue.
- The integration could generate a time-lapse that only includes the commits related to a specific Jira issue.
- The generated video could be attached as a comment to the Jira issue, providing a visual summary of the work done.
- A "View Time-Lapse" button could be added to the Jira issue screen.

## 3. Requirements

- **Dependencies:**
    - The Jira REST API for interacting with Jira issues.
- A mechanism to parse commit messages and extract Jira issue keys.
- The integration needs to handle authentication with Jira.
- It should be configurable to connect to different Jira instances (Cloud or Server).

## 4. Limitations

- The accuracy of the time-lapse depends on the developers consistently referencing Jira issue keys in their commit messages.
- The initial version might only support Jira Cloud.
- Generating and uploading videos for every commit could be resource-intensive and might clutter the Jira issue. The integration should be designed to be non-intrusive, perhaps generating the time-lapse on demand or when the issue is closed.
