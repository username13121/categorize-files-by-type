# Categorize files by type script
Recursively scans all subfolders and files within the given folder. Categorizes all files based on their 
file extensions. Returns a dictionary where the keys are file extensions (e.g., .txt, .pdf, .jpg) and 
the values are lists of full paths to the files with those extensions.


## Installation:
```commandline
git clone https://github.com/username13121/categorize-files-by-type.git
cd categorize-files-by-type
```

## Quick run
Scan current directory

```commandline
python -m CategorizeFilesByType
```

## Basic usage
```python
from TestCategorizeFilesByType import categorize_files_by_type

folder_name='TestTask'

result = categorize_files_by_type(folder_name)
print(result)
```

## Tests

```commandline
python -m unittest
```