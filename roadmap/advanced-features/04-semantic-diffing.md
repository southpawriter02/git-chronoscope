# Semantic Diffing

## 1. Feature Description

This feature goes beyond simple text-based diffs and visualizes changes in a way that understands the structure and syntax of the code. For example, renaming a function would be shown as a "rename" operation, not as a deletion and an addition of lines.

## 2. Intended Functionality

- The tool will parse the code into an Abstract Syntax Tree (AST).
- It will compare the ASTs of a file between two commits to identify structural changes.
- The visualization will use this information to provide a more meaningful representation of the changes, such as:
    - Highlighting moved code blocks.
    - Indicating renamed variables, functions, or classes.
    - Collapsing purely cosmetic changes (e.g., reformatting).

## 3. Requirements

- **Dependencies:**
    - A library for parsing the programming languages used in the repository (e.g., `tree-sitter`, `ANTLR`).
    - A library or algorithm for comparing ASTs.
- This feature requires significant processing power and memory.

## 4. Limitations

- Supporting multiple programming languages can be challenging, as each language requires its own parser.
- The initial implementation might only support a single language (e.g., Python or JavaScript).
- Semantic diffing can be complex and may not always produce perfect results.
- The performance will be a major concern, and this feature might be best suited for smaller repositories or for analyzing specific commits rather than generating a full time-lapse.
