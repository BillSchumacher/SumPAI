import os

from loguru import logger

from sum_pai.process.file import process_file


def process_directory(directory_path: str) -> None:
    """Processes all Python files within a directory and its subdirectories.

    Args:
        directory_path (str): The path to the directory containing Python files
          to process.
    """
    logger.info(f"Processing directory {directory_path}")
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                process_file(file_path)
