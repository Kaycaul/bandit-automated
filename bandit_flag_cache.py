import json
import os
import warnings
from bandit_constants import FLAG_CACHE_PATH


def get_cached_flags() -> dict[str, str]:
    try:
        with open(FLAG_CACHE_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def get_cached_flag(username: str) -> str | None:
    flags = get_cached_flags()
    if username not in flags.keys():
        return None
    else:
        flag = flags[username]
        print(f"Found cached flag for {username}: {nice_flag_print(flag)}")
        return flag


def cache_flag(username: str, flag: str):
    if not flag:
        warnings.warn(
            f"Flag for {username} is empty! This may indicate an error or a regression."
        )
    print(f"Caching flag for {username}: {nice_flag_print(flag)}")
    flags = get_cached_flags()
    flags[username] = flag
    with open(FLAG_CACHE_PATH, "w") as f:
        f.write(json.dumps(flags, indent=4))


def summarize_flag_cache():
    flags = get_cached_flags()
    print(f"Cache contains {len(flags)} flags:")
    for username, flag in flags.items():
        print(f"  {username.upper()}:{" "*(10-len(username))}{nice_flag_print(flag)}")


def nice_flag_print(flag: str) -> str:
    return flag.strip() if len(flag) <= 40 else f"{flag.replace('\n', '\\n')[:40]}..."


def clear_flag_cache():
    if os.path.exists(FLAG_CACHE_PATH):
        os.remove(FLAG_CACHE_PATH)
