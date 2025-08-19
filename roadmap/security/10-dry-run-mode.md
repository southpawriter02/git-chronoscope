# 10: "Dry Run" Mode

## Description
This feature provides a "dry run" or "preview" mode where the agent describes the sequence of actions it intends to take without actually executing them. This allows the user to review and approve the agent's entire plan before any changes are made to the codebase.

## Expected Behaviors
- The user can start a session in "dry run" mode.
- In this mode, when the agent decides to use a tool that modifies the state (e.g., `create_file_with_block`, `run_in_bash_session`), it will simulate the action instead of executing it.
- The simulation will produce a log of intended actions, such as "Would create file `path/to/file.py`" or "Would run command `npm install`".
- The agent will proceed through its entire workflow based on the *expected* outcomes of these simulated actions.
- At the end of the dry run, the user is presented with the full plan and can then choose to execute it for real.

## Limitations
- **Simulation Inaccuracy:** A dry run is a simulation. The agent's prediction of a command's outcome might not match the real-world result. For example, a command might fail in reality due to an environmental issue that wasn't modeled in the simulation.
- **Complex Interactions:** It can be very difficult to accurately simulate the side effects of complex commands or scripts.
- **State Dependency:** The agent's plan might change based on the real-time output of a command. A dry run cannot fully capture this dynamic, potentially leading to a different execution path in the real run.

## Requirements
- A way to intercept tool calls and replace their execution with a simulation.
- A "simulation engine" that can predict the likely outcome of common actions (e.g., creating a file results in the file existing; running `npm install` results in a `node_modules` directory).
- A clear user interface to distinguish between a dry run and a real execution.

## Possible Issues
- **Divergence between Dry Run and Real Run:** The most significant risk is that the actual execution behaves differently from the dry run preview, leading to unexpected and potentially harmful outcomes.
- **User Misunderstanding:** Users might place too much trust in the dry run, treating it as a guarantee of the outcome rather than an educated guess.
- **Implementation Complexity:** Building a reliable simulation for a wide range of shell commands and tools is extremely challenging.
