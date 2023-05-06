import os
import pickle

import cityhash

from sum_pai.embedding.length_safe import len_safe_get_embedding


def save_or_load_embedding(element):
    city_hash = cityhash.CityHash64(element["summary"])
    output_name = f"{element['name']}__{city_hash}.sumpai"

    if os.path.exists(output_name):
        with open(output_name, "rb") as input_file:
            loaded_element = pickle.load(input_file)
            element["embedding"] = loaded_element["embedding"]
    else:
        element["embedding"] = len_safe_get_embedding(
            f"Summary: {element['summary']} " f"Code: {element['source_code']}"
        )
        with open(output_name, "wb") as output_file:
            pickle.dump(element, output_file)
