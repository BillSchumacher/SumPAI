import os
import pickle

import click
import numpy as np
from loguru import logger

from sum_pai.create_search_embedding import create_search
from sum_pai.embedding.convert import convert_embeddings_to_np


@click.command()
@click.option(
    "--text", prompt="Enter the text to search for", help="Text to search for."
)
@click.option(
    "--target", prompt="Enter the target directory", help="The project to scan."
)
@click.option("--search-type", default="svm", help="The type of search to perform.")
def main(text: str, target: str, search_type: str):
    """
    Summarizes the input text and creates a search embedding.

    Args:
        text (str): The text to be summarized and used to create an embedding.
        target (str): The project to scan.
        search_type (str): The type of search to perform.
    """
    return search_project(text, target, search_type)


def search_project(text: str, target: str, search_type: str):
    """
    Summarizes the input text and creates a search embedding.

    Args:
        text (str): The text to be summarized and used to create an embedding.
        target (str): The project to scan.
        search_type (str): The type of search to perform.
    """
    logger.info(f"Searching for {text} in {target}")
    search_embedding = create_search(text)
    summaries = []
    for root, dirs, files in os.walk(target):
        for file in files:
            if file.endswith(".sumpai"):
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as f:
                    summaries.append(pickle.load(f))
    embeddings = [summary["embedding"] for summary in summaries]
    logger.debug(f"Embeddings: {len(embeddings)}")

    vector = None
    for embed in embeddings:
        logger.debug(f"Chunked Embeddings: {len(embed[1])}")
        embed = convert_embeddings_to_np(embed[0][0])
        logger.debug(f"Chunked Embedding: {len(embed)}")
        embed = embed[np.newaxis, :]
        if vector is None:
            vector = embed
        else:
            vector = np.concatenate(
                [
                    vector,
                    embed,
                ],
                axis=0,
            )
    logger.debug(f"Vector: {vector.shape}")

    if search_type == "knn":
        from sum_pai.search.knn import knn_search

        result = knn_search(vector, search_embedding["embedding"])
    elif search_type == "svm":
        from sum_pai.search.svm import svm_search

        result = svm_search(vector, search_embedding["embedding"])
    else:
        raise ValueError(f"Invalid search type: {search_type}")
    logger.debug(f"result: {result}")
    logger.info(f"Search complete for {text} in {target}")
    logger.info("Results:")
    summary_found = summaries[result[0]]
    logger.info(f"File: {summary_found['path']} Text: {summary_found['summary']}")


if __name__ == "__main__":
    main()
