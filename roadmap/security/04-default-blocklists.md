# 04: Default Blocklists for Files and Commands

## Description
This feature provides a built-in, non-optional blocklist of sensitive file paths and dangerous shell commands that the agent is forbidden from accessing or executing. This serves as a baseline layer of security, independent of any user-configured rules like `.agentignore`.

## Expected Behaviors
- **File Access:** The agent should be hard-coded to deny access to a list of common sensitive filenames and directories, such as `.env`, `.ssh/`, `id_rsa`, `credentials.json`, `*.pem`, `.aws/`, etc. This check should occur before any user-defined rules.
- **Command Execution:** The agent's shell environment should prevent the execution of a predefined list of high-risk commands. This list could include commands used for networking (`ssh`, `scp`, `curl`, `wget`, `nc`), privilege escalation (`sudo`), or destructive actions (`rm -rf /`).
- These blocklists should be active by default and not require any user configuration.

## Limitations
- **Inflexibility:** A hard-coded blocklist might be too restrictive for certain advanced use cases where an agent legitimately needs to use a command like `curl` to download a resource.
- **Completeness:** It is impossible to create a blocklist that covers every possible dangerous command or sensitive filename. Attackers can often find obscure commands or rename sensitive files to bypass such lists.

## Requirements
- A well-researched and maintained list of sensitive file patterns and dangerous commands.
- The blocklist logic must be deeply integrated into the tool-handling and shell execution modules and must not be bypassable by the agent's reasoning process.
- A mechanism for updating these lists as new threats or patterns emerge.

## Possible Issues
- **Breaking Legitimate Workflows:** The agent might be unable to complete a legitimate task if it requires access to a file or command on the blocklist. For example, a project's build script might legitimately use `curl`.
- **False Sense of Security:** A default blocklist is a good baseline, but it should not be considered a complete security solution. Users might become complacent and neglect other important security measures.
- **Maintenance Burden:** The lists will need to be reviewed and updated regularly to remain effective.
