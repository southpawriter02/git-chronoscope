# 06: Filesystem Sandboxing

## Description
This feature ensures that the agent can only read and write files within the repository's designated working directory. It provides a strong guarantee that the agent cannot access or modify any other part of the filesystem on the machine where it is running.

## Expected Behaviors
- The agent's process should be confined to a specific directory using a filesystem sandbox or jail (e.g., a `chroot` jail or a container mount).
- All file-related tools (`read_file`, `ls`, `create_file_with_block`, etc.) should operate relative to this sandboxed root.
- Any attempt by the agent or a tool it uses to access a path outside of the sandbox (e.g., `/etc/passwd`, `~/.ssh`) must fail.
- The sandbox should prevent path traversal attacks (e.g., `../../...`) by its very nature.

## Limitations
- **Configuration Complexity:** Setting up and managing filesystem sandboxes can be complex and platform-dependent.
- **Legitimate Access:** Some legitimate build tools or compilers may need access to libraries or resources outside the project directory. This would require carefully managed exceptions or mounting specific external directories into the sandbox as read-only.

## Requirements
- A sandboxing mechanism that can be reliably and securely applied to the agent's execution environment. This is often provided by the underlying containerization or virtualization technology (e.g., Docker, gVisor).
- The agent's file-access tools must be designed to work within this sandboxed environment.
- The entry point for the agent must ensure that the process is correctly placed inside the sandbox before any code execution begins.

## Possible Issues
- **"Leaky" Sandboxes:** A misconfigured sandbox could have "holes" that allow an attacker to escape to the host filesystem. The security of this feature is entirely dependent on the correctness of its implementation.
- **Performance:** Filesystem operations within a sandboxed environment can sometimes be slower than native operations, though this overhead is usually minimal with modern technologies.
- **Tool Incompatibility:** Some third-party tools may not function correctly when they detect they are running in a restricted filesystem or `chroot` jail.
