import sys
import shutil
from bandit_levels import get_solvers, SolverType
from typing import List
from bandit_flag_cache import (
    get_cached_flag,
    cache_flag,
    clear_flag_cache,
    summarize_flag_cache,
)

if "--summary" in sys.argv:
    summarize_flag_cache()
    exit(0)

if "--fresh" in sys.argv:
    clear_flag_cache()
    shutil.rmtree("./tmp", ignore_errors=True)

current_password = "bandit0"
solvers: List[SolverType] = get_solvers()
for level, solver in enumerate(solvers):
    # look for a saved flag for this level
    flag = get_cached_flag(f"bandit{level}")
    # if not found, run the solver and save the flag
    if flag is None:
        flag = solver(current_password)
        cache_flag(f"bandit{level}", flag)
    # use this flag as the password for the next level
    current_password = flag

summarize_flag_cache()
