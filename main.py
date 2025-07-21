from bandit_client import (
    get_cached_flag,
    cache_flag,
    summarize_flag_cache,
)
from bandit_levels import (
    levels,
)

current_password = "bandit0"
for level, solver in enumerate(levels):
    # look for a saved flag for this level
    flag = get_cached_flag(f"bandit{level}")
    # if not found, run the solver and save the flag
    if flag is None:
        flag = solver(current_password)
        cache_flag(f"bandit{level}", flag)
    # use this flag as the password for the next level
    current_password = flag

summarize_flag_cache()