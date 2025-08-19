# 05: Restricted Shell for Commands

## Description
This feature ensures that all shell commands executed by the agent run in a restricted, sandboxed shell environment rather than a standard shell like `bash` or `zsh`. This environment strictly limits which system calls can be made, which binaries can be executed, and what parts of the filesystem are accessible.

## Expected Behaviors
- The agent's `run_in_bash_session` tool should execute commands within a purpose-built, locked-down shell.
- The shell should enforce a strict allow-list of safe commands (e.g., `ls`, `cat`, `echo`, `grep`, package managers) rather than relying on a blocklist of dangerous ones.
- Filesystem access from within the shell should be constrained to the repository's working directory. Any attempt to access parent directories (`..`) or absolute paths (`/`) should be blocked.
- The environment should have no network access unless explicitly enabled via other security features (like Network Egress Control).

## Limitations
- **Compatibility:** Many standard shell scripts and build tools rely on features of `bash` or other common shells. A highly restricted shell might not be able to run them without modification.
- **Complexity of Implementation:** Building and maintaining a secure, restricted shell environment is a complex task that requires deep expertise in systems security.

## Requirements
- A sandboxing technology to create the restricted shell environment (e.g., using technologies like `chroot`, containers, or specialized libraries).
- A well-defined allow-list of commands and system calls that are considered safe for the agent to use.
- Extensive testing to ensure the sandbox is not escapable.

## Possible Issues
- **Environment Brittleness:** A very restrictive environment might break in unexpected ways when encountering complex or unusual shell commands, making it difficult for the agent to perform its tasks.
- **Maintenance:** The allowed command list and environment capabilities will need to be maintained and updated as new, safe tools become necessary for common development tasks.
- **Finding the Right Balance:** Making the shell too restrictive will render the agent useless for many tasks. Making it too permissive will defeat the purpose of the security feature.
