from typing import Dict, List, Union

from sum_pai.code_extractor import CodeExtractor
from sum_pai.embedding.loading import load_embedding


def process_functions(
    extractor: CodeExtractor, path: str
) -> List[Dict[str, Union[str, float]]]:
    """
    Process the functions from the code extractor and save or load their embeddings.

    Args:
        extractor (CodeExtractor): The code extractor containing the functions
            to process.
        path (str): The path to the directory where embeddings are saved or loaded from.

    Returns:
        List[Dict[str, Union[str, float]]]: A list of dictionaries containing
            information about the functions and their embeddings.
    """

    return [
        load_embedding(function_source, "function", function_name, path)
        for function_name, function_source in extractor.functions.items()
    ]
