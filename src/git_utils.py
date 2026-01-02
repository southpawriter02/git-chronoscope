import git
import fnmatch
from typing import List, Optional, Dict

class GitRepo:
    """
    A class to interact with a Git repository.
    """
    def __init__(self, repo_path: str):
        """
        Initializes the GitRepo object.

        :param repo_path: Path to the Git repository.
        """
        try:
            self.repo = git.Repo(repo_path)
        except git.exc.InvalidGitRepositoryError:
            raise ValueError(f"'{repo_path}' is not a valid Git repository.")
        except git.exc.NoSuchPathError:
            raise FileNotFoundError(f"The path '{repo_path}' does not exist.")

    def get_commit_history(self, branch: str = None):
        """
        Gets the commit history of a given branch.

        :param branch: The name of the branch to get the history from. Defaults to the active branch.
        :return: A list of dictionaries, where each dictionary represents a commit.
        """
        if branch is None:
            try:
                branch = self.repo.active_branch.name
            except TypeError:
                # Detached HEAD state
                branch = self.repo.head.commit.hexsha

        try:
            commits = list(self.repo.iter_commits(branch, reverse=True))
        except git.exc.GitCommandError:
            # A common case is that the default branch is 'master' not 'main'
            if branch == 'main':
                try:
                    commits = list(self.repo.iter_commits('master', reverse=True))
                except git.exc.GitCommandError:
                    raise ValueError("Could not find branch 'main' or 'master'. Please specify a branch.")
            else:
                raise ValueError(f"Could not find branch '{branch}'.")

        history = []
        for commit in commits:
            history.append({
                'hash': commit.hexsha[:7],
                'author_name': commit.author.name,
                'author_email': commit.author.email,
                'date': commit.committed_datetime,
                'message': commit.message.strip(),
                'commit_obj': commit, # Keep the commit object for later use
            })
        return history

    def get_file_tree_at_commit(self, commit_obj):
        """
        Gets the file tree of the repository at a specific commit, including file content.

        :param commit_obj: The commit object from GitPython.
        :return: A dictionary mapping file paths to their content.
        """
        tree = commit_obj.tree
        file_contents = {}
        # Recursively traverse the tree
        for item in tree.traverse():
            if item.type == 'blob':  # 'blob' represents a file
                # Decode the file content to a string, handling potential binary files
                try:
                    file_contents[item.path] = item.data_stream.read().decode('utf-8')
                except UnicodeDecodeError:
                    # If it's not a UTF-8 text file, we can either skip it or mark it as binary.
                    file_contents[item.path] = "[Binary File]"
        return file_contents

    def filter_file_tree(
        self,
        file_tree: Dict[str, str],
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """
        Filter a file tree based on include/exclude glob patterns.

        :param file_tree: Dictionary mapping file paths to their content.
        :param include_patterns: List of glob patterns to include. If provided, only matching files are kept.
        :param exclude_patterns: List of glob patterns to exclude. Matching files are removed.
        :return: Filtered dictionary of file paths to content.
        """
        if not include_patterns and not exclude_patterns:
            return file_tree

        filtered = {}
        for path, content in file_tree.items():
            # Check include patterns - if provided, file must match at least one
            if include_patterns:
                included = any(
                    fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(path.split('/')[-1], pattern)
                    for pattern in include_patterns
                )
                if not included:
                    continue

            # Check exclude patterns - if file matches any, skip it
            if exclude_patterns:
                excluded = any(
                    fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(path.split('/')[-1], pattern)
                    for pattern in exclude_patterns
                )
                if excluded:
                    continue

            filtered[path] = content

        return filtered

    def get_changed_files_in_commit(self, commit_obj) -> List[str]:
        """
        Get the list of files that were changed in a specific commit.

        :param commit_obj: The commit object from GitPython.
        :return: A list of file paths that were added, modified, or deleted.
        """
        changed_files = []

        # For the initial commit, all files in the tree are "changed"
        if not commit_obj.parents:
            for item in commit_obj.tree.traverse():
                if item.type == 'blob':
                    changed_files.append(item.path)
        else:
            # Compare with the first parent
            parent = commit_obj.parents[0]
            diff = parent.diff(commit_obj)
            for diff_item in diff:
                if diff_item.a_path:
                    changed_files.append(diff_item.a_path)
                if diff_item.b_path and diff_item.b_path != diff_item.a_path:
                    changed_files.append(diff_item.b_path)

        return changed_files

    def commit_affects_filtered_paths(
        self,
        commit_obj,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None
    ) -> bool:
        """
        Check if a commit affects any files matching the filter patterns.

        :param commit_obj: The commit object from GitPython.
        :param include_patterns: List of glob patterns to include.
        :param exclude_patterns: List of glob patterns to exclude.
        :return: True if the commit affects at least one file matching the filter criteria.
        """
        if not include_patterns and not exclude_patterns:
            return True  # No filtering, all commits are relevant

        changed_files = self.get_changed_files_in_commit(commit_obj)

        for path in changed_files:
            # Check include patterns
            if include_patterns:
                included = any(
                    fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(path.split('/')[-1], pattern)
                    for pattern in include_patterns
                )
                if not included:
                    continue

            # Check exclude patterns
            if exclude_patterns:
                excluded = any(
                    fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(path.split('/')[-1], pattern)
                    for pattern in exclude_patterns
                )
                if excluded:
                    continue

            # This file matches the filter criteria
            return True

        return False
