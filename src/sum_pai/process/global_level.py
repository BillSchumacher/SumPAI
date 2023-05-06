from typing import Dict, Union

from sum_pai.code_extractor import CodeExtractor
from sum_pai.embedding.loading import load_embedding


def process_global_level_code(
    extractor: CodeExtractor, path: str
) -> Dict[str, Union[str, float]]:
    """
    Process the global level code from the code extractor and save or load its
        embedding.

    Args:
        extractor (CodeExtractor): The code extractor containing the global level code
            to process.
        path (str): The path to the directory where embeddings are saved or loaded from.

    Returns:
        Dict[str, Union[str, float]]: A dictionary containing information about the
            global level code and its embedding.
    """

    global_level_code = "\n".join(extractor.global_level_code)
    return load_embedding(global_level_code, "global", "global", path)
