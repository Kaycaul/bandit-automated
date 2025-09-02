import io
import subprocess
import time
from typing import List
import warnings
from paramiko import (
    AuthenticationException,
    Channel,
    SSHClient,
    AutoAddPolicy,
    SSHException,
    RSAKey,
)
from bandit_constants import BANDIT_HOST, BANDIT_PORT_SSH


class BanditClient:
    __client: SSHClient
    __shell: Channel = None  # not initialized until needed

    def __init__(
        self,
        username: str,
        password: str = None,
        key: str = None,
        hostname: str = BANDIT_HOST,
        port: int = BANDIT_PORT_SSH,
    ):
        if not password and not key:
            raise Exception("Must provide password or key")
        if password and key:
            raise warnings.warn("Both password and key provided, using password")
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        print(f"Connecting to {username}@{hostname}:{port}")
        while True:
            try:
                if password:
                    client.connect(
                        hostname=hostname,
                        port=port,
                        username=username,
                        password=password,
                    )
                else:
                    client.connect(
                        hostname=hostname,
                        port=port,
                        username=username,
                        pkey=RSAKey.from_private_key(io.StringIO(key)),
                    )
                break
            except AuthenticationException:
                if password:
                    print(f"Authentication failed using password: \"{password}\"")
                else:
                    print(f"Authentication failed using key: \"{key}\"")
                raise
            except (ConnectionResetError, SSHException):
                print("Connection reset, trying again...")
        print("Connection established")
        self.__client = client

    def run(self, cmd: str) -> str:
        _, stdout, stderr = self.__client.exec_command(cmd)
        err = stderr.read().decode("utf-8")
        if err:
            print(err)
        return stdout.read().decode("utf-8")

    def download_file(self, remote_file: str, destination: str = ".") -> None:
        print(f"Downloading {remote_file}")
        with self.__client.open_sftp() as sftp:
            sftp.get(
                remote_file,
                destination,
                callback=lambda transferred, total: print(
                    f"Downloaded {transferred/total*100}%", end="\r"
                ),
            )
        print(f"\n{remote_file} saved to {destination}")

    # send individual keystrokes to a persistent shell
    # expectation: wait for this string as a signal to return
    # timeout: number of seconds to wait before raising
    # returns: the output of the shell
    def send_keystrokes(
        self, keystrokes: str, expectation: str, timeout: int = 5
    ) -> str:
        time_waited = 0
        shell = self.__get_shell()
        shell.send(keystrokes)
        res = ""
        while True:
            if not shell.recv_ready():
                if time_waited > timeout:
                    print(res)
                    raise Exception(f"Timed out after {timeout} seconds")
                time.sleep(0.05)
                time_waited += 0.05
                continue
            res += shell.recv(1024).decode("utf-8")
            if expectation in res:
                return res

    # clones a repo by sending keystrokes to ignore fingerprint and send password
    def git_clone(self, repo_url: str, password: str) -> str:
        tmp = self.run("mktemp -d").strip()
        self.send_keystrokes(
            f"git clone {repo_url} {tmp}\n",
            expectation="(yes/no/[fingerprint])?",
        )
        self.send_keystrokes(
            "yes\n",
            expectation="password:",
        )
        self.send_keystrokes(
            f"{password}\n",
            expectation=":~$",
        )
        return tmp

    # big bad, but this might be needed sometimes
    # dont use this unless you really need to
    def _get(self) -> SSHClient:
        return self.__client

    # initialize the shell on demand
    def __get_shell(self) -> Channel:
        if not self.__shell:
            self.__shell = self.__client.invoke_shell()
        return self.__shell

    def __del__(self):
        self.__client.close()


def run_remote_command(
    command: str,
    username: str,
    password: str,
    hostname: str = BANDIT_HOST,
    port: int = BANDIT_PORT_SSH,
) -> str:
    with SSHClient() as client:
        client.set_missing_host_key_policy(AutoAddPolicy())
        print(f"Connecting to {username}@{hostname}:{port}")
        while True:
            try:
                client.connect(
                    hostname=hostname, port=port, username=username, password=password
                )
                break
            except AuthenticationException:
                print(f"Authentication failed using password: {password}")
                raise
            except (ConnectionResetError, SSHException):
                print("Connection reset, trying again...")
        print("Parsing result")
        _, stdout, _ = client.exec_command(command)
        return stdout.read().decode("utf-8")


def run_command(command: str, quiet: bool = True) -> str:
    run_command_with_args(command.split(), quiet=quiet)


def run_command_with_args(args: List[str], quiet: bool = True) -> str:
    res = subprocess.run(args)
    if res.stderr and not quiet:
        print(res.stderr.decode("utf-8"))
    if res.stdout:
        return res.stdout.decode("utf-8")
    else:
        return ""
