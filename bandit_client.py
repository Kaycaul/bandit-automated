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
