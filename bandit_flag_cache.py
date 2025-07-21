import json, os
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
        print(f"Found cached flag for {username}: {flag}")
        return flag
    
def cache_flag(username: str, flag: str):
    print(f"Caching flag for {username}: {flag}")
    flags = get_cached_flags()
    flags[username] = flag
    with open(FLAG_CACHE_PATH, "w") as f:
        f.write(json.dumps(flags, indent=4))

def summarize_flag_cache():
    flags = get_cached_flags()
    print(f"Cache contains {len(flags)} flags:")
    for username, flag in flags.items():
        print(f"  {username.upper()}:{" "*(10-len(username))}{flag}")

def clear_flag_cache():
    if os.path.exists(FLAG_CACHE_PATH):
        os.remove(FLAG_CACHE_PATH)