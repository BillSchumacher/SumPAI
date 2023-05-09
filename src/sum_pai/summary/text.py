from loguru import logger

from sum_pai.summary.chat_completion import chat_completion


def summarize_text(text: str) -> str:
    """Generates a summary for the given text using OpenAI's ChatCompletion.

    Args:
        text (str): The text to summarize.

    Returns:
        str: The generated summary of the text.
    """
    logger.info("Summarizing text")
    return chat_completion(f"Extract the main features:\n\n{text}")
