"""Handler for patching save data"""

import hashlib
from typing import Union
from . import helper

def get_md5_sum(save_data: bytes, game_version: str) -> str:
    """Get the md5 sum of the save data"""

    if game_version == "jp":
        game_version = ""
    salt = bytes("battlecats" + game_version, "utf-8")
    data_to_hash = salt + save_data[:-32]

    return hashlib.md5(data_to_hash).hexdigest()


def detect_game_version(save_data: bytes) -> Union[None, str]:
    """Detect the game version of the save file"""

    game_versions = ["jp", "en", "kr", "tw"]
    curr_hash = save_data[-32::]
    curr_hash_str = str(curr_hash, "utf-8")

    for game_version in game_versions:
        hash_str = get_md5_sum(save_data, game_version)
        if hash_str == curr_hash_str:
            return game_version
    return None


def patch_save_data(save_data: bytes, game_version: str) -> bytes:
    """Set the md5 sum of the save data"""

    save_hash = get_md5_sum(save_data, game_version)
    hash_bytes = bytes(save_hash, "utf-8")

    return helper.set_range(save_data, hash_bytes, len(save_data) - 32)
