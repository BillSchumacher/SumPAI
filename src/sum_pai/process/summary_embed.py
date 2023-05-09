from typing import Any, Dict, Optional

import cityhash
from loguru import logger

from sum_pai.embedding.length_safe import len_safe_get_embedding
from sum_pai.summary.code import summarize_code
from sum_pai.summary.text import summarize_text


def summarize_and_embed(
    source: str,
    source_type: str,
    name: str,
    path: str,
    summary: Optional[str] = None,
    city_hash: Optional[int] = None,
) -> Dict[str, Any]:
    """Generates a summary and embedding for the given source code and returns the
      result as a dictionary.

    Args:
        source (str): The source code to summarize and embed.
        source_type (str): The type of the source code (e.g., 'class', 'function').
        name (str): The name of the code element.
        path (str): The file path of the code element.

    Returns:
        Dict[str, Any]: A dictionary containing the type, name, path,
          summary, and embedding of the code element.
    """
    logger.info(
        f"Summarizing and embedding code for: {name} path:"
        f" {path} type: {source_type}"
    )
    system = None
    if summary is None:
        if source_type == "directory":
            summary = summarize_text(source)
        else:
            summary = summarize_code(source, system=system)
    if city_hash is None:
        city_hash = cityhash.CityHash64(source)
    embedding = len_safe_get_embedding(f"Summary: {summary} Code: {source}")
    return {
        "type": source_type,
        "name": name,
        "path": path,
        "hash": city_hash,
        "summary": summary,
        "embedding": embedding,
    }
