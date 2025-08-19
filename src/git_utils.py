import git

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
            branch = self.repo.active_branch.name

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
