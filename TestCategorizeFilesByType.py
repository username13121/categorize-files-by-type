import os
import tempfile
import unittest
from datetime import datetime, timedelta
from typing import Dict, List
from CategorizeFilesByType import categorize_files_by_type


class TestCategorizeFilesByType(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    # Generate files out of given data
    def generate_files(self, files: Dict[str, List]):
        for file_name, (size_kib, mtime) in files.items():
            file = os.path.join(self.temp_dir.name, file_name)

            # Create a directory if it doesn't exist
            os.makedirs(os.path.dirname(file), exist_ok=True)

            with open(file, 'wb') as f:
                # Write random data of specified size into file
                f.write(os.urandom(size_kib * 1024))

            # Set specified file creation and modification time
            os.utime(file, (mtime.timestamp(), mtime.timestamp()))

    def test_no_filters_no_exts(self):
        files_info = {
            'file0': [0, datetime.now()],
            'file1': [0, datetime.now()],
            'file2': [0, datetime.now()],
            'file3': [0, datetime.now()]
        }
        self.generate_files(files_info)
        result = categorize_files_by_type(self.temp_dir.name)

        # Check if result's length is the same
        self.assertEqual(len(files_info), len(result['']))

        # Check if every file is present
        for file_name in files_info:
            file = os.path.join(self.temp_dir.name, file_name)
            self.assertIn(file, result[''])

    # Different extensions test
    def test_exts(self):
        files_info = {
            'file0.txt': [0, datetime.now()],
            'file1.png': [0, datetime.now()],
            'file2.pdf': [0, datetime.now()],
            'file3': [0, datetime.now()]
        }
        self.generate_files(files_info)

        result = categorize_files_by_type(self.temp_dir.name)

        # Checking if 4 categories created for 4 different filetypes
        self.assertEqual(len(files_info), len(result))

        # Checking if all files fell into their respective categories
        for file_name in files_info:
            file = os.path.join(self.temp_dir.name, file_name)
            _, ext = os.path.splitext(file)
            self.assertIn(file, result[ext])

    # Size filters test
    def test_size(self):
        files_info = {
            'big': [100, datetime.now()],
            'medium': [10, datetime.now()],
            'small': [1, datetime.now()]
        }
        self.generate_files(files_info)

        result_big = categorize_files_by_type(self.temp_dir.name, max_size_kib=20)
        result_small = categorize_files_by_type(self.temp_dir.name, min_size_kib=5)

        # Checking if big file was filtered out
        self.assertNotIn(
            os.path.join(self.temp_dir.name, 'big'),
            result_big[''])

        # Checking if big file was filtered out
        self.assertNotIn(os.path.join(self.temp_dir.name, 'small'),
                         result_small[''])

        # Checking if medium file is present in both tests
        self.assertIn(
            os.path.join(self.temp_dir.name, 'medium'),
            result_big[''], result_small['']
        )

    # Date filters test
    def test_date(self):
        files_info = {
            'week_after': [0, datetime.now() + timedelta(weeks=1)],
            'today': [0, datetime.now()],
            'week_ago': [0, datetime.now() - timedelta(weeks=1)]
        }
        self.generate_files(files_info)

        result_week_after = categorize_files_by_type(self.temp_dir.name, max_mtime=datetime.now() + timedelta(days=1))
        result_week_ago = categorize_files_by_type(self.temp_dir.name, min_mtime=datetime.now() - timedelta(days=1))

        # Check if the newest file was filtered
        self.assertNotIn(
            os.path.join(self.temp_dir.name, 'week_after'),
            result_week_after[''])

        # Check if the oldest file was filtered
        self.assertNotIn(os.path.join(self.temp_dir.name, 'week_ago'),
                         result_week_ago[''])

        # Check if today's file present in both tests
        self.assertIn(
            os.path.join(self.temp_dir.name, 'today'),
            result_week_after[''], result_week_ago['']
        )

    # Directory depth test
    def test_depth(self):
        depth = 10
        files_info = {
            'file0': [0, datetime.now()],
            'file1': [0, datetime.now()],
            'file2': [0, datetime.now()],
            'file3': [0, datetime.now()],
            'file4': [0, datetime.now()],
        }

        # files placed at every depth
        files_info_deep = {}
        for file_name in files_info:
            for i in range(depth):
                files_info_deep[file_name] = [0, datetime.now()]
                file_name = f'dir{i}\\{file_name}'
        self.generate_files(files_info_deep)
        result = categorize_files_by_type(self.temp_dir.name)

        # Check if result's length is the same
        self.assertEqual(len(files_info_deep), len(result['']))

        # Check if all files are present
        for file_name, _ in files_info_deep.items():
            file = os.path.join(self.temp_dir.name, file_name)
            self.assertIn(file, result[''])

    def test_invalid_directory(self):
        with self.assertRaises(FileNotFoundError):
            categorize_files_by_type('invalid_directory')

    def test_not_directory(self):
        file = os.path.join(self.temp_dir.name, 'file')

        with open(file, 'w') as f:
            f.write('')

        with self.assertRaises(NotADirectoryError):
            categorize_files_by_type(file)
