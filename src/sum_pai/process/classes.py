from typing import Dict, List, Union

from sum_pai.code_extractor import CodeExtractor
from sum_pai.embedding.loading import load_embedding


def process_classes(
    extractor: CodeExtractor, path: str
) -> List[Dict[str, Union[str, float]]]:
    """
    Process the classes from the code extractor and save or load their embeddings.

    Args:
        extractor (CodeExtractor): The code extractor containing the classes to process.
        path (str): The path to the directory where embeddings are saved or loaded from.

    Returns:
        List[Dict[str, Union[str, float]]]: A list of dictionaries containing
            information about the classes and their embeddings.
    """

    code_elements = []
    for class_name, class_info in extractor.classes.items():
        code = class_info["source_code"]
        code_elements.append(load_embedding(code, "class", class_name, path))
        code_elements.extend(
            load_embedding(
                function_source,
                "class_function",
                f"{class_name}__{function_name}",
                path,
            )
            for function_name, function_source in class_info["functions"].items()
        )
    return code_elements
