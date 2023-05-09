from typing import Optional

from loguru import logger

from sum_pai.summary.chat_completion import chat_completion


def summarize_code(code: str, system: Optional[str]) -> str:
    """Generates a summary for the given Python code using ChatCompletion.

    Args:
        code (str): The Python code to summarize.

    Returns:
        str: The generated summary of the code.
    """
    logger.info("Summarizing code")
    return chat_completion(
        f"{code}\n\nWhat are the key features from this information?"
        " Only list the features, do not number them, and provide a use case.",
        system=system,
    )
