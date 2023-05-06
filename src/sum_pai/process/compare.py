from typing import Any, Dict, Union

from sum_pai.file_io import load_sum


def same_hash(
    value: str, name: str, path: str, path_is_full: bool = False
) -> Union[Dict[str, Any], bool]:
    """
    Check if the hash value of a code element is the same as the stored hash value
    and return the loaded summary if the hash values are the same.

    Args:
        value (str): Hash value to compare.
        name (str): Name of the code element.
        path (str): Path to the stored summary file.
        path_is_full (bool, optional): If True, the path is treated as a full path.
            If False, the path is constructed as "{path}__{name}.sumpai". Default is False.

    Returns:
        Union[Dict[str, Any], bool]: Loaded summary if the hash values are the same,
            False otherwise.
    """
    full_path = path if path_is_full else f"{path}__{name}.sumpai"
    if loaded_sum := load_sum(full_path):
        loaded_hash = loaded_sum["hash"]
        if value == loaded_hash:
            return loaded_sum
    return False
