import cityhash

from sum_pai.file_io import load_sum


def same_hash(value, name, path) -> bool:
    if class_sum := load_sum(f"{path}__{name}.sumpai"):
        loaded_hash = class_sum["hash"]
        if value == loaded_hash:
            return True
    return False
