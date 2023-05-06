from typing import List, Optional, Tuple

import numpy as np
from loguru import logger

from sum_pai.constants import EMBEDDING_CTX_LENGTH, EMBEDDING_ENCODING, EMBEDDING_MODEL
from sum_pai.embedding.batch import chunked_tokens
from sum_pai.embedding.create import get_embedding


def len_safe_get_embedding(
    text: str,
    model: str = EMBEDDING_MODEL,
    max_tokens: int = EMBEDDING_CTX_LENGTH,
    encoding_name: str = EMBEDDING_ENCODING,
    average: bool = True,
    hashed_key: Optional[str] = None,
) -> Tuple[List[List[float]], List[float]]:
    """Generates an embedding for the given text, handling text that exceeds the
      maximum token length.

    Args:
        text (str): The text to generate the embedding for.
        model (str, optional): The name of the embedding model.
          Defaults to EMBEDDING_MODEL.
        max_tokens (int, optional): The maximum number of tokens for the embedding
          context. Defaults to EMBEDDING_CTX_LENGTH.
        encoding_name (str, optional): The name of the text encoding.
          Defaults to EMBEDDING_ENCODING.
        average (bool, optional): Whether to return the average of embeddings or not.
          Defaults to True.
        hashed_key (Optional[str], optional): An optional hashed key for caching.
          Defaults to None.

    Returns:
        Tuple[List[List[float]], List[float]]: A tuple containing the chunk embeddings
          and the averaged embeddings.
    """
    logger.debug(
        f"Text: {text} \n\nEncoding: {encoding_name}\n "
        f"Chunk Length: {max_tokens} \nAverage: {average}"
        f" \nHashed Key: {hashed_key}"
    )
    chunk_embeddings = []
    chunk_lens = []
    for chunk in chunked_tokens(
        text, encoding_name=encoding_name, chunk_length=max_tokens
    ):
        chunk_embeddings.append(
            get_embedding(chunk, model=model, hashed_key=hashed_key)
        )
        chunk_lens.append(len(chunk))
    averaged_embeddings = []
    if average:
        averaged_embeddings = np.average(chunk_embeddings, axis=0, weights=chunk_lens)
        # normalizes length to 1
        averaged_embeddings = averaged_embeddings / np.linalg.norm(averaged_embeddings)
        averaged_embeddings = averaged_embeddings.tolist()
    return chunk_embeddings, averaged_embeddings
