# "solver" functions that solve bandit levels, use the previous flag and extract the current flag
import re
from bandit_client import run_remote_command

def bandit0(password):
    cmd = "cat ~/readme"
    readme_text = run_remote_command(command=cmd, username="bandit0", password=password)
    return re.search(r"The password you are looking for is: (.{32})\n", readme_text).group(1)

def bandit1(password):
    cmd = "cat ~/-"
    flag = run_remote_command(command=cmd, username="bandit1", password=password).strip()
    return flag

def bandit2(password):
    cmd = r"cat ~/spaces\ in\ this\ filename"
    flag = run_remote_command(command=cmd, username="bandit2", password=password).strip()
    return flag

# this is the order that the solvers will be called in, essentially piped together
levels = [
    bandit0,
    bandit1,
    bandit2,
]