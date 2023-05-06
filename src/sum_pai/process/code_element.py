import ast
from typing import Dict, List, Union

from sum_pai.code_extractor import CodeExtractor
from sum_pai.process.classes import process_classes
from sum_pai.process.functions import process_functions
from sum_pai.process.global_level import process_global_level_code


def process_code_elements(code: str, path: str) -> List[Dict[str, Union[str, float]]]:
    """
    Process the given code to extract code elements, including classes, class functions,
    functions, and global level code, and save or load their embeddings.

    Args:
        code (str): The source code to process.
        path (str): The path to the directory where embeddings are saved or loaded from.

    Returns:
        List[Dict[str, Union[str, float]]]: A list of dictionaries containing
            information about the code elements and their embeddings.
    """

    extractor = CodeExtractor()
    tree = ast.parse(code)
    extractor.visit(tree)
    extractor.extract_global_level_code(tree)

    code_elements = process_classes(extractor, path)
    code_elements.extend(process_functions(extractor, path))
    code_elements.append(process_global_level_code(extractor, path))
    return code_elements
