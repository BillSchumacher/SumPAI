from itertools import islice
from typing import Any, Iterable, Iterator, List, Tuple

import tiktoken
from loguru import logger


def batched(iterable: Iterable, n: int) -> Iterator[Tuple]:
    """Batch data into tuples of length n. The last batch may be shorter.

    Args:
        iterable (Iterable): The iterable to be batched.
        n (int): The length of each batch.

    Yields:
        Iterator[Tuple]: Tuples containing the batched data.
    """
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def chunked_tokens(text: str, encoding_name: str, chunk_length: int) -> Iterator:
    """Divide text into chunks of tokens with the specified length.

    Args:
        text (str): The text to be tokenized and chunked.
        encoding_name (str): The name of the encoding to use for tokenization.
        chunk_length (int): The maximum number of tokens in each chunk.

    Yields:
        Iterator: An iterator containing chunks of tokens.
    """
    logger.debug(
        f"Text: {text} \n\nEncoding: {encoding_name}\n" f"Chunk Length: {chunk_length}"
    )
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    yield from batched(tokens, chunk_length)


def create_chunks(text: str, n: int, tokenizer: Any) -> Iterator[List[int]]:
    """Split a text into smaller chunks of size n, preferably ending at the
    end of a sentence.

    Args:
        text (str): The text to be split into chunks.
        n (int): The target chunk size in tokens.
        tokenizer (Tokenizer): The tokenizer used to tokenize the text.

    Yields:
        Iterator[List[int]]: An iterator containing chunks of token IDs.
    """
    tokens = tokenizer.encode(text)
    i = 0
    while i < len(tokens):
        # Find the nearest end of sentence within a range of 0.5 * n and 1.5 * n tokens
        j = min(i + int(1.5 * n), len(tokens))
        while j > i + int(0.5 * n):
            # Decode the tokens and check for full stop or newline
            chunk = tokenizer.decode(tokens[i:j])
            if chunk.endswith(".") or chunk.endswith("\n"):
                break
            j -= 1
        # If no end of sentence found, use n tokens as the chunk size
        if j == i + int(0.5 * n):
            j = min(i + n, len(tokens))
        yield tokens[i:j]
        i = j
