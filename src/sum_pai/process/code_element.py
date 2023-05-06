import ast
from typing import Dict, List, Union

import cityhash
from importlib_metadata import _top_level_declared

from sum_pai.code_extractor import CodeExtractor
from sum_pai.file_io import load_sum
from sum_pai.process.compare import same_hash
from sum_pai.process.summary_embed import summarize_and_embed


def process_code_elements(code: str, path: str) -> List[Dict[str, Union[str, float]]]:
    """Processes classes and functions in the given code and generates summaries
        and embeddings.

    Args:
        code (str): The source code to process.

    Returns:
        List[Dict[str, Union[str, float]]]: A list of dictionaries containing
            information about the classes and functions in the code, including their
              type, name, summary, and embedding.
    """
    extractor = CodeExtractor()
    tree = ast.parse(code)
    extractor.visit(tree)
    extractor.extract_global_level_code(tree)

    code_elements = []

    for class_name, class_info in extractor.classes.items():
        code = class_info["source_code"]
        city_hash = cityhash.CityHash64(code)
        if same_hash(city_hash, class_name, path):
            continue
        code_elements.append(
            summarize_and_embed(code, "class", class_name, path, city_hash=city_hash)
        )
        for function_name, function_source in class_info["functions"].items():
            class_function_name = f"{class_name}__{function_name}"
            city_hash = cityhash.CityHash64(function_source)
            if same_hash(city_hash, class_function_name, path):
                continue
            code_elements.append(
                summarize_and_embed(
                    function_source,
                    "class_function",
                    class_function_name,
                    path,
                    city_hash=city_hash,
                )
            )

    for function_name, function_source in extractor.functions.items():
        city_hash = cityhash.CityHash64(function_source)
        if same_hash(city_hash, function_name, path):
            continue
        code_elements.append(
            summarize_and_embed(
                function_source,
                "function",
                function_name,
                path,
                city_hash=city_hash,
            )
        )
    _global_level_code = "\n".join(extractor.global_level_code)
    city_hash = cityhash.CityHash64(_global_level_code)
    if not same_hash(city_hash, "global", path):
        code_elements.append(
            summarize_and_embed(
                _global_level_code,
                "global",
                "global",
                path,
                city_hash=city_hash,
            )
        )
    return code_elements
