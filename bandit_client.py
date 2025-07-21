import json
from paramiko import AuthenticationException, SSHClient, AutoAddPolicy, SSHException
from bandit_constants import BANDIT_HOST, BANDIT_PORT_SSH, FLAG_CACHE_PATH

def run_remote_command(command, username, password, hostname=BANDIT_HOST, port=BANDIT_PORT_SSH):
    with SSHClient() as client:
        client.set_missing_host_key_policy(AutoAddPolicy())
        print(f"Connecting to {username}@{hostname}:{port}")
        while True:
            try:
                client.connect(hostname=hostname, port=port, username=username, password=password)
                break
            except AuthenticationException:
                print(f"Authentication failed using password: {password}")
                raise
            except (ConnectionResetError, SSHException):
                print("Connection reset, trying again...")
        print(f"Parsing result")
        _, stdout, _ = client.exec_command(command)
        return stdout.read().decode("utf-8")

def get_cached_flags():
    try:
        with open(FLAG_CACHE_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def get_cached_flag(username):
    flags = get_cached_flags()
    if username not in flags.keys():
        return None
    else:
        flag = flags[username]
        print(f"Using cached flag for {username}: {flag}")
        return flag
    
def cache_flag(username, flag):
    print(f"Caching flag for {username}: {flag}")
    flags = get_cached_flags()
    flags[username] = flag
    with open(FLAG_CACHE_PATH, "w") as f:
        f.write(json.dumps(flags, indent=4))

def summarize_flag_cache():
    flags = get_cached_flags()
    print(f"Flag cache contains {len(flags)} flags")
    for username, flag in flags.items():
        print(f"  {username.upper()}: {flag}")