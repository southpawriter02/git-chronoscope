# Visual Studio Code Extension

## 1. Feature Description

This feature provides a Visual Studio Code extension that allows users to generate and view git time-lapses directly within the editor.

## 2. Intended Functionality

- A new command in the VS Code command palette to generate a time-lapse for the current project.
- A dedicated view in the sidebar to configure and control the time-lapse generation.
- An integrated video player to watch the generated time-lapse without leaving the editor.
- The ability to generate a time-lapse for a specific file or a selection of code.
- Integration with the source control view to visualize the history of a branch or a pull request.

## 3. Requirements

- **Dependencies:**
    - The VS Code Extension API.
    - A way to bundle the Git Time-Lapse tool with the extension or to call it as an external process.
- The extension needs to be published to the Visual Studio Code Marketplace.
- It should work on all platforms supported by VS Code (Windows, macOS, Linux).

## 4. Limitations

- The performance of the extension might be a concern, especially when generating large time-lapses, as it could block the UI thread of the editor. The generation process should run in the background.
- The integrated video player might have limited features compared to a standalone player.
- The initial version might not have all the intended functionalities, focusing on the basic generation and viewing of time-lapses.
