from venv import logger

import openai


def summarize_code(text: str) -> str:
    """Generates a summary for the given Python code using OpenAI's Davinci Codex.

    Args:
        text (str): The Python code to summarize.

    Returns:
        str: The generated summary of the code.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarize the following Python code:"},
            {"role": "user", "content": text},
        ],
        max_tokens=256,
        n=1,
        stop=None,
        temperature=0.5,
    )
    logger.debug(f"Summarization response: {response}")
    return response.choices[0].message["content"].strip()


def summarize_text(text: str) -> str:
    """Generates a summary for the given Python code using OpenAI's Davinci Codex.

    Args:
        text (str): The Python code to summarize.

    Returns:
        str: The generated summary of the code.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarize the following:"},
            {"role": "user", "content": text},
        ],
        max_tokens=512,
        n=1,
        stop=None,
        temperature=0.5,
    )
    logger.debug(f"Summarization response: {response}")
    return response.choices[0].message["content"].strip()
