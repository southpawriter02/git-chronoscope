# Author Highlighting

## 1. Feature Description

This feature highlights the contributions of different authors in the time-lapse video. It helps in visualizing who worked on which parts of the codebase and at what time.

## 2. Intended Functionality

- Each author in the repository will be assigned a unique color.
- When a file is modified by an author, the changes (or the file itself) will be highlighted with the author's assigned color.
- The video could include a legend that maps colors to author names.
- Users should be able to filter the time-lapse to show the contributions of specific authors only.

## 3. Requirements

- A mechanism to identify the author of each line of code or each file. `git blame` can be used for this purpose.
- A color generation algorithm to assign distinct colors to authors.
- The rendering engine needs to support text highlighting or changing the color of UI elements based on the author.

## 4. Limitations

- `git blame` can be slow on large files or repositories with a long history. This might significantly impact the performance of the time-lapse generation.
- Attributing code to the correct author can be tricky, especially after large refactorings or code movements. The accuracy of the highlighting will depend on the accuracy of `git blame`.
- In the initial version, the color palette might be fixed and not customizable by the user.
