import re, json
from bandit_client import run_remote_command, get_cached_flag, cache_flag, summarize_flag_cache
from bandit_constants import FLAG_CACHE_PATH

password = get_cached_flag("bandit0")
flag = get_cached_flag("bandit1")
if flag is None:
    readme_text = run_remote_command(command="cat ~/readme", username="bandit0", password=password)
    flag = re.search(r"The password you are looking for is: (.{32})\n", readme_text).group(1)
    cache_flag("bandit1", flag)

password = flag
flag = get_cached_flag("bandit2")
if flag is None:
    flag = run_remote_command(command=r"cat ~/-", username="bandit1", password=password).strip()
    cache_flag("bandit2", flag)

password = flag
flag = get_cached_flag("bandit3")
if flag is None:
    flag = run_remote_command(command=r"cat ~/spaces\ in\ this\ filename", username="bandit2", password=password).strip()
    cache_flag("bandit3", flag)

summarize_flag_cache()