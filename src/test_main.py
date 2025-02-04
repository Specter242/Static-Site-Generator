import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import shutil
from main import copyall, extract_title

class TestMainFunctions(unittest.TestCase):

    # @patch('os.path.exists')
    # @patch('os.makedirs')
    # @patch('shutil.rmtree')
    # @patch('shutil.copy2')
    # @patch('os.listdir')
    # def test_copyall(self, mock_listdir, mock_copy2, mock_rmtree, mock_makedirs, mock_exists):
    #     # Setup mock responses
    #     mock_exists.side_effect = lambda path: path == "source"
    #     mock_listdir.return_value = ["file1.txt", "dir1"]
        
    #     # Mock for os.path.isdir
    #     with patch('os.path.isdir') as mock_isdir:
    #         mock_isdir.side_effect = lambda path: path == "source/dir1"
            
    #         # Call the function
    #         copyall("source", "destination")
            
    #         # Assertions
    #         mock_exists.assert_any_call("source")
    #         mock_exists.assert_any_call("destination")
    #         mock_rmtree.assert_called_once_with("destination")
    #         mock_makedirs.assert_called_once_with("destination")
    #         mock_copy2.assert_called_once_with("source/file1.txt", "destination/file1.txt")
    #         mock_listdir.assert_called_once_with("source")
    #         mock_isdir.assert_any_call("source/dir1")

    def test_extract_title(self):
        markdown = "# Title\nSome content"
        title = extract_title(markdown)
        self.assertEqual(title, "Title")

    def test_extract_title_no_title(self):
        markdown = "Some content without title"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_multiple_titles(self):
        markdown = "# Title1\nSome content\n# Title2\nMore content"
        title = extract_title(markdown)
        self.assertEqual(title, "Title1")

    def test_extract_title_different_header_levels(self):
        markdown = "## Subtitle\nSome content\n# Title\nMore content"
        title = extract_title(markdown)
        self.assertEqual(title, "Title")

    def test_extract_title_empty_string(self):
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == '__main__':
    unittest.main()