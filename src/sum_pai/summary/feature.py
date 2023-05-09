from loguru import logger

from sum_pai.summary.chat_completion import chat_completion


def summarize_features(summaries: str) -> str:
    """Summarize features for the given feature summaries using ChatCompletion.

    Args:
        summaries (str): The summaries to summarize features for.

    Returns:
        str: The features summarized from of the summaries.
    """
    logger.info("Summarizing features")
    return chat_completion(
        f"Arrange the following by category and list the key features:\n\n{summaries}"
    )
