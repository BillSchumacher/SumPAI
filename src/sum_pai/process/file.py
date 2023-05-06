from pathlib import Path
from typing import Optional

import cityhash

from sum_pai.file_io import load_sum, save_sum
from sum_pai.process.code_element import process_code_elements
from sum_pai.process.compare import same_hash
from sum_pai.process.summary_embed import summarize_and_embed
from sum_pai.summary.text import summarize_text


def process_file(file_path: str) -> Optional[str]:
    """
    Processes a Python file, generating summaries and embeddings for its elements.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        Optional[str]: Summary of the file. Returns None if the file is empty.
    """
    with open(file_path, "r") as file:
        code = file.read()
    if not len(code):
        return
    path = Path(file_path)

    city_hash = cityhash.CityHash64(code)
    path_no_ext = file_path[:-3]
    existing_output_name = f"{path_no_ext}.sumpai"
    if loaded_sum := same_hash(
        city_hash, "file", existing_output_name, path_is_full=True
    ):
        return loaded_sum["summary"]
    code_elements = process_code_elements(code, str(path))
    summaries = [element["summary"] for element in code_elements]
    file_summary = summarize_text("\n".join(summaries))

    save_sum(
        existing_output_name,
        summarize_and_embed(code, "file", path.name, path_no_ext, file_summary),
    )
    for element in code_elements:
        output_name = f"{path_no_ext}__{element['name']}.sumpai"
        save_sum(output_name, element)
    return file_summary
