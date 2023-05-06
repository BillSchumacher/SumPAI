import os

import cityhash
from loguru import logger

from sum_pai.file_io import save_sum
from sum_pai.process.compare import same_hash
from sum_pai.process.file import process_file
from sum_pai.process.summary_embed import summarize_and_embed
from sum_pai.summary.text import summarize_text


def process_directory(directory_path: str) -> None:
    """Processes all Python files within a directory and its subdirectories.

    Args:
        directory_path (str): The path to the directory containing Python files
          to process.
    """
    logger.info(f"Processing directory {directory_path}")

    file_summaries = {}
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                if file_summary := process_file(file_path):
                    file_summaries[file_path] = file_summary
    logger.info(f"Processed {len(file_summaries)} files")
    collated_summary = "\n".join(
        [
            f"{file_path}: {file_summary}\n"
            for file_path, file_summary in file_summaries.items()
        ]
    )
    logger.debug(f"Collated summary:\n{collated_summary}")
    city_hash = cityhash.CityHash64(collated_summary)
    existing_output_name = f"{directory_path}__dir_overview.sumpai"
    if same_hash(city_hash, "dir_overview", existing_output_name, path_is_full=True):
        return
    summary = summarize_text(collated_summary)
    logger.debug(f"Summary:\n{summary}")
    save_sum(
        existing_output_name,
        summarize_and_embed(
            collated_summary, "directory", "dir_overview", directory_path, summary
        ),
    )
