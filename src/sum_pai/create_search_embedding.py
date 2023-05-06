import click
import os
import pickle
import cityhash
from sum_pai.embedding.convert import convert_embeddings_to_np
from sum_pai.embedding.length_safe import len_safe_get_embedding

from sum_pai.summary.text import summarize_text


@click.command()
@click.option("--text", prompt="Enter the text to summarize and create an embedding", 
              help="Text to summarize and create an embedding.")
def main(text: str):
    return create_search(text)


def create_search(text: str):
    """
    Summarizes the input text and creates a search embedding.

    Args:
        text (str): The text to be summarized and used to create an embedding.
    """

    city_hash = cityhash.CityHash64(text)
    file_name = f"search_embedding_{city_hash}.pickle"
    if os.path.exists(file_name):
        print(f"Search embedding already exists for {text}")
        return pickle.load(open(file_name, "rb"))
    
    # Summarize the input text
    summary = summarize_text(text)
    print(f"Summary: {summary}")

    # Create the search embedding
    _, embedding = len_safe_get_embedding(text)
    # len_safe_get_embedding(f"Summary: {summary} Code: {text}")

    # Convert the embedding to a NumPy array and print it
    embedding_array = convert_embeddings_to_np(embedding)
    search_embedding = {
        "embedding": embedding_array,
        "summary": summary,
        "text": text
    }
    with open(file_name, "wb") as f:
        pickle.dump(search_embedding, f)
    print(f"Search embedding created for {text}")
    return search_embedding


if __name__ == "__main__":
    main()
