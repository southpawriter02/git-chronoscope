import unittest
from unittest.mock import patch, MagicMock, call
from src import main

class TestMainCli(unittest.TestCase):

    @patch('sys.argv', ['src/main.py', 'fake_repo', 'output.mp4', '--fps', '5'])
    @patch('src.main.GitRepo')
    @patch('src.main.FrameRenderer')
    @patch('src.main.VideoEncoder')
    @patch('src.main.tempfile.mkdtemp', return_value='fake_temp_dir')
    @patch('src.main.shutil.rmtree')
    def test_main_orchestration(self, mock_rmtree, mock_mkdtemp, mock_video_encoder, mock_frame_renderer, mock_git_repo):
        # --- Mock instances and their methods ---
        mock_repo_instance = MagicMock()
        mock_git_repo.return_value = mock_repo_instance

        mock_commit1 = {
            'hash': '1234567',
            'author_name': 'Test Author',
            'author_email': 'test@example.com',
            'date': 'some_date',
            'message': 'Initial commit',
            'commit_obj': MagicMock()
        }
        mock_commit2 = {
            'hash': 'abcdefg',
            'author_name': 'Test Author',
            'author_email': 'test@example.com',
            'date': 'some_other_date',
            'message': 'Second commit',
            'commit_obj': MagicMock()
        }
        mock_repo_instance.get_commit_history.return_value = [mock_commit1, mock_commit2]

        mock_repo_instance.get_file_tree_at_commit.side_effect = [
            {'file1.txt': 'content1'},
            {'file1.txt': 'content1', 'file2.txt': 'content2'}
        ]

        mock_renderer_instance = MagicMock()
        mock_frame_renderer.return_value = mock_renderer_instance

        mock_frame_image = MagicMock()
        mock_renderer_instance.render_frame.return_value = mock_frame_image

        mock_encoder_instance = MagicMock()
        mock_video_encoder.return_value = mock_encoder_instance

        # --- Run the main function ---
        main.main()

        # --- Assertions ---
        mock_git_repo.assert_called_once_with('fake_repo')
        mock_frame_renderer.assert_called_once_with(
            width=1920,
            height=1080,
            bg_color='#141618',
            text_color='#FFFFFF',
            font_path=None,
            font_size=15,
            no_email=False
        )
        mock_repo_instance.get_commit_history.assert_called_once_with(branch=None)

        # Check calls to render_frame using a direct comparison of call_args_list
        self.assertEqual(mock_renderer_instance.render_frame.call_count, 2)

        # The DataRedactor will be called, but since there are no secrets, the data is unchanged.
        # The `commit_obj` is not passed to render_frame.
        sanitized_commit1 = mock_commit1.copy()
        del sanitized_commit1['commit_obj']
        sanitized_commit2 = mock_commit2.copy()
        del sanitized_commit2['commit_obj']

        # The content of the files should also be sanitized
        sanitized_contents1 = {'file1.txt': 'content1'}
        sanitized_contents2 = {'file1.txt': 'content1', 'file2.txt': 'content2'}

        self.assertEqual(
            mock_renderer_instance.render_frame.call_args_list,
            [
                call(sanitized_commit1, sanitized_contents1),
                call(sanitized_commit2, sanitized_contents2)
            ]
        )

        # Check that frames were saved
        mock_frame_image.save.assert_has_calls([
            call('fake_temp_dir/frame_00000.png'),
            call('fake_temp_dir/frame_00001.png')
        ])

        mock_video_encoder.assert_called_once_with('output.mp4', frame_rate=5, format='mp4')
        mock_encoder_instance.create_video_from_frames.assert_called_once_with([
            'fake_temp_dir/frame_00000.png',
            'fake_temp_dir/frame_00001.png'
        ])

        mock_rmtree.assert_called_once_with('fake_temp_dir')

    @patch('sys.argv', ['src/main.py', 'fake_repo', 'output.mp4', '--no-email'])
    @patch('src.main.GitRepo')
    @patch('src.main.FrameRenderer')
    @patch('src.main.VideoEncoder')
    @patch('src.main.tempfile.mkdtemp', return_value='fake_temp_dir')
    @patch('src.main.shutil.rmtree')
    def test_main_with_no_email_flag(self, mock_rmtree, mock_mkdtemp, mock_video_encoder, mock_frame_renderer, mock_git_repo):
        # We only need to test that the `no_email` flag is passed correctly
        mock_repo_instance = MagicMock()
        mock_git_repo.return_value = mock_repo_instance
        mock_commit = {
            'hash': '123',
            'author_name': 'Test Author',
            'author_email': 'test@example.com',
            'date': 'some_date',
            'message': 'Test commit',
            'commit_obj': MagicMock()
        }
        mock_repo_instance.get_commit_history.return_value = [mock_commit]
        mock_repo_instance.get_file_tree_at_commit.return_value = {}

        main.main()

        mock_frame_renderer.assert_called_once()
        # Get the keyword arguments passed to the FrameRenderer constructor
        kwargs = mock_frame_renderer.call_args.kwargs
        self.assertTrue(kwargs.get('no_email', False))

if __name__ == '__main__':
    unittest.main()
