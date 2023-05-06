import os
import pickle
from pathlib import Path

import cityhash

from sum_pai.file_io import load_sum, save_sum
from sum_pai.process.code_element import process_code_elements
from sum_pai.process.summary_embed import summarize_and_embed
from sum_pai.summary.text import summarize_text


def process_file(file_path):
    with open(file_path, "r") as file:
        code = file.read()
    if not len(code):
        return
    path = Path(file_path)

    city_hash = cityhash.CityHash64(code)
    path_no_ext = file_path[:-3]
    existing_output_name = f"{path_no_ext}.sumpai"
    loaded_sum = load_sum(existing_output_name)
    if loaded_sum:
        loaded_hash = loaded_sum["hash"]
        if city_hash == loaded_hash:
            return
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
