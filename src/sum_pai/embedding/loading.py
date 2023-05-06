import cityhash
from loguru import logger

from sum_pai.process.compare import same_hash
from sum_pai.process.summary_embed import summarize_and_embed


def load_embedding(code, code_type, obj_name, path, path_is_full=False):
    city_hash = cityhash.CityHash64(code)
    if loaded_sum := same_hash(city_hash, obj_name, path, path_is_full):
        logger.debug(f"Loaded {loaded_sum} from {path}")
        return loaded_sum
    return summarize_and_embed(code, code_type, obj_name, path, city_hash=city_hash)
