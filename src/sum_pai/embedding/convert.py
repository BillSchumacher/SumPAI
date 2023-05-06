from typing import List

import numpy as np


def convert_embeddings_to_np(embeddings: List[List[float]]) -> np.ndarray:
    """Converts a list of embeddings to a NumPy array of float32 dtype.

    Args:
        embeddings (List[List[float]]): A list of embeddings to be converted.

    Returns:
        np.ndarray: A NumPy array containing the embeddings with float32 dtype.
    """
    return np.array(embeddings).astype(np.float32)
