import os
from typing import Optional, Dict, List
from datetime import datetime
import logging
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG, filename='categorize_files_by_type.log', filemode='w',
                    format='%(asctime)s %(levelname)s: %(message)s', encoding='utf-8')


def categorize_files_by_type(
        folder_path: str,
        min_size_kib: Optional[float] = None,
        max_size_kib: Optional[float] = None,
        min_mtime: Optional[datetime] = None,
        max_mtime: Optional[datetime] = None
) -> Dict[str, List[str]]:
    """
    Recursively scans all subfolders and files within the given folder. Categorizes all files based on their
    file extensions. Returns a dictionary where the keys are file extensions (e.g., .txt, .pdf, .jpg) and the values
    are lists of full paths to the files with those extensions.

    :param str folder_path: Relative or absolute path to the folder
    :param float min_size_kib: Minimum size of files to scan in KiB
    :param float max_size_kib: Maximum size of files to scan in KiB
    :param datetime min_mtime: Minimum modified time of files to scan
    :param datetime max_mtime: Maximum modified time of files to scan

    :returns: Dictionary of file paths sorted by their extensions

    :raises FileNotFound: No such path
    :raises NotADirectory: File found, not a directory
    """

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f'{folder_path} does not exist ')
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f'{folder_path} is not a directory')

    # Get absolute path
    folder_path = os.path.abspath(folder_path)

    # Default datatype for dictionary to append values
    files_dict = defaultdict(list)

    logging.info(f'Directory: "{folder_path}": Starting to process')

    for path, _, file_names in os.walk(folder_path):
        logging.info(f'Subdirectory "{os.path.relpath(path, folder_path)}": Processing')

        for file_name in file_names:
            file = os.path.join(path, file_name)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file))

            file_size_kib = os.path.getsize(file) / 1024

            # Filters check
            if (
                    (min_size_kib is not None and
                     file_size_kib < min_size_kib) or

                    (max_size_kib is not None and
                     file_size_kib > max_size_kib) or

                    (min_mtime is not None and
                     file_mtime < min_mtime) or

                    (max_mtime is not None and
                     file_mtime > max_mtime)):
                logging.debug(f'File "{file_name}": Criteria mismatch, skipping')
                continue

            file_extension = os.path.splitext(file_name)[1]
            files_dict[file_extension].append(file)
            logging.debug(f'File "{file_name}" added to "{file_extension}" category')
    logging.info(f'Directory "{folder_path}": Finished Processing')

    # Covert to standard dictionary
    return dict(files_dict)
