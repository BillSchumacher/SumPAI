import numpy as np


def knn_search(embeddings, query) -> np.ndarray:
    """Performs a search using KNN."""
    similarities = embeddings.dot(query)
    return np.argsort(-similarities)
