# Branch Comparison

## 1. Feature Description

This feature enables users to create a time-lapse that visualizes the differences between two branches. This is particularly useful for understanding the evolution of a feature branch compared to the main branch, or for visualizing the changes in a pull request.

## 2. Intended Functionality

- The tool will accept two branch names as input.
- It will generate a side-by-side or a split-screen video that shows the state of the two branches at corresponding points in time.
- The "corresponding points in time" could be defined by commit timestamps or by finding equivalent commits based on commit history (e.g., using `git merge-base`).
- The visualization should highlight the differences between the files on the two branches.

## 3. Requirements

- The tool needs to be able to check out and inspect two different branches simultaneously.
- A diffing algorithm to identify and visualize the differences between the files.
- The rendering engine must support a split-screen or side-by-side layout.

## 4. Limitations

- Accurately aligning the history of two branches can be complex, especially if they have diverged significantly. The initial implementation might use a simple timestamp-based alignment.
- Visualizing the differences for large-scale refactorings or file renames can be challenging.
- This feature might be significantly slower than a single-branch time-lapse due to the need to process two branches and compute diffs.
