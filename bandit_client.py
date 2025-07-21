import io, subprocess
from paramiko import AuthenticationException, SSHClient, AutoAddPolicy, SSHException, RSAKey
from bandit_constants import BANDIT_HOST, BANDIT_PORT_SSH

def run_remote_command(command: str,
                       username: str,
                       password: str,
                       hostname: str=BANDIT_HOST,
                       port: int=BANDIT_PORT_SSH
                       ) -> str:
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

def run_remote_command_using_key(command: str,
                       username: str,
                       key: str,
                       hostname: str=BANDIT_HOST,
                       port: int=BANDIT_PORT_SSH
                       ) -> str:
    with SSHClient() as client:
        client.set_missing_host_key_policy(AutoAddPolicy())
        print(f"Connecting to {username}@{hostname}:{port}")
        while True:
            try:
                client.connect(hostname=hostname, port=port, username=username, pkey=RSAKey.from_private_key(io.StringIO(key)))
                break
            except AuthenticationException:
                raise
            except (ConnectionResetError, SSHException):
                print("Connection reset, trying again...")
        print(f"Parsing result")
        _, stdout, _ = client.exec_command(command)
        return stdout.read().decode("utf-8")

def run_command(command: str) -> None:
    print(command)
    subprocess.run(command.split())

def download_file(remote_file: str,
                  destination: str,
                  username: str,
                  password: str,
                  hostname: str=BANDIT_HOST,
                  port: int=BANDIT_PORT_SSH
                  ) -> None:
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
        print(f"Downloading file: {remote_file}")
        with client.open_sftp() as sftp:
            sftp.get(remote_file, destination)
