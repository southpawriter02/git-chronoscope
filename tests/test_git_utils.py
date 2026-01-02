import unittest
import tempfile
import shutil
import os
from git import Repo
from src.git_utils import GitRepo

class TestGitRepo(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

        # Initialize a new Git repository in the temporary directory
        self.repo = Repo.init(self.test_dir)

        # Create some commits
        self.commit_hashes = []
        for i in range(3):
            file_name = f'file_{i}.txt'
            file_path = os.path.join(self.test_dir, file_name)
            with open(file_path, 'w') as f:
                f.write(f'This is file {i}')
            self.repo.index.add([file_path])
            commit = self.repo.index.commit(f'Commit {i}')
            self.commit_hashes.append(commit.hexsha)

    def tearDown(self):
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)

    def test_init_valid_repo(self):
        git_repo = GitRepo(self.test_dir)
        self.assertIsNotNone(git_repo.repo)

    def test_init_invalid_repo(self):
        # Create a non-git directory
        non_git_dir = os.path.join(self.test_dir, 'not_a_repo')
        os.makedirs(non_git_dir)
        with self.assertRaises(ValueError):
            GitRepo(non_git_dir)

    def test_init_nonexistent_path(self):
        with self.assertRaises(FileNotFoundError):
            GitRepo('/path/to/nonexistent/repo')

    def test_get_commit_history(self):
        git_repo = GitRepo(self.test_dir)
        # The default branch can be 'master' or 'main' depending on git version
        branch_name = git_repo.repo.active_branch.name
        history = git_repo.get_commit_history(branch=branch_name)

        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]['message'], 'Commit 0')
        self.assertEqual(history[1]['message'], 'Commit 1')
        self.assertEqual(history[2]['message'], 'Commit 2')
        self.assertEqual(history[0]['hash'], self.commit_hashes[0][:7])

    def test_get_file_tree_at_commit(self):
        git_repo = GitRepo(self.test_dir)
        branch_name = git_repo.repo.active_branch.name
        history = git_repo.get_commit_history(branch=branch_name)

        # Test tree at the first commit
        commit0 = history[0]['commit_obj']
        file_tree0 = git_repo.get_file_tree_at_commit(commit0)
        self.assertEqual(file_tree0, {'file_0.txt': 'This is file 0'})

        # Test tree at the second commit
        commit1 = history[1]['commit_obj']
        file_tree1 = git_repo.get_file_tree_at_commit(commit1)
        self.assertEqual(file_tree1, {'file_0.txt': 'This is file 0', 'file_1.txt': 'This is file 1'})

        # Test tree at the last commit
        commit2 = history[2]['commit_obj']
        file_tree2 = git_repo.get_file_tree_at_commit(commit2)
        self.assertEqual(file_tree2, {'file_0.txt': 'This is file 0', 'file_1.txt': 'This is file 1', 'file_2.txt': 'This is file 2'})

    def test_filter_file_tree_include_pattern(self):
        """Test filtering file tree with include patterns."""
        git_repo = GitRepo(self.test_dir)
        
        # Create a mock file tree
        file_tree = {
            'src/main.py': 'python code',
            'src/utils.py': 'utils code',
            'tests/test_main.py': 'test code',
            'README.md': 'readme',
            'config.json': 'config'
        }
        
        # Test include *.py - should keep all .py files
        result = git_repo.filter_file_tree(file_tree, include_patterns=['*.py'])
        self.assertEqual(set(result.keys()), {'src/main.py', 'src/utils.py', 'tests/test_main.py'})
        
        # Test include src/* - should keep only files in src
        result = git_repo.filter_file_tree(file_tree, include_patterns=['src/*'])
        self.assertEqual(set(result.keys()), {'src/main.py', 'src/utils.py'})

    def test_filter_file_tree_exclude_pattern(self):
        """Test filtering file tree with exclude patterns."""
        git_repo = GitRepo(self.test_dir)
        
        file_tree = {
            'src/main.py': 'python code',
            'src/utils.py': 'utils code',
            'tests/test_main.py': 'test code',
            'README.md': 'readme',
            'debug.log': 'log content'
        }
        
        # Test exclude *.log
        result = git_repo.filter_file_tree(file_tree, exclude_patterns=['*.log'])
        self.assertNotIn('debug.log', result)
        self.assertEqual(len(result), 4)
        
        # Test exclude tests/*
        result = git_repo.filter_file_tree(file_tree, exclude_patterns=['tests/*'])
        self.assertNotIn('tests/test_main.py', result)

    def test_filter_file_tree_combined_patterns(self):
        """Test filtering with both include and exclude patterns."""
        git_repo = GitRepo(self.test_dir)
        
        file_tree = {
            'src/main.py': 'code',
            'src/debug.py': 'debug',
            'tests/test_main.py': 'test',
            'README.md': 'readme'
        }
        
        # Include *.py but exclude debug*
        result = git_repo.filter_file_tree(
            file_tree,
            include_patterns=['*.py'],
            exclude_patterns=['*debug*']
        )
        self.assertEqual(set(result.keys()), {'src/main.py', 'tests/test_main.py'})

    def test_get_changed_files_in_commit(self):
        """Test getting changed files in a commit."""
        git_repo = GitRepo(self.test_dir)
        branch_name = git_repo.repo.active_branch.name
        history = git_repo.get_commit_history(branch=branch_name)
        
        # First commit should have the initial file
        commit0 = history[0]['commit_obj']
        changed0 = git_repo.get_changed_files_in_commit(commit0)
        self.assertIn('file_0.txt', changed0)
        
        # Second commit should have file_1.txt as changed
        commit1 = history[1]['commit_obj']
        changed1 = git_repo.get_changed_files_in_commit(commit1)
        self.assertIn('file_1.txt', changed1)

    def test_commit_affects_filtered_paths(self):
        """Test checking if a commit affects filtered paths."""
        git_repo = GitRepo(self.test_dir)
        branch_name = git_repo.repo.active_branch.name
        history = git_repo.get_commit_history(branch=branch_name)
        
        # All commits affect *.txt files
        for commit in history:
            affects = git_repo.commit_affects_filtered_paths(
                commit['commit_obj'],
                include_patterns=['*.txt']
            )
            self.assertTrue(affects)
        
        # No commits affect *.py files
        for commit in history:
            affects = git_repo.commit_affects_filtered_paths(
                commit['commit_obj'],
                include_patterns=['*.py']
            )
            self.assertFalse(affects)

if __name__ == '__main__':
    unittest.main()
