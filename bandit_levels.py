# "solver" functions that solve bandit levels, use the previous flag and extract the current flag
import re, os, shutil, paramiko, io
from bandit_client import (
    run_remote_command,
    download_file,
    run_command,
    run_remote_command_using_key,
)

def bandit0(password: str):
    cmd = "cat ~/readme"
    readme_text = run_remote_command(command=cmd, username="bandit0", password=password)
    return re.search(r"The password you are looking for is: (.{32})\n", readme_text).group(1)

def bandit1(password: str):
    cmd = "cat ~/-"
    flag = run_remote_command(command=cmd, username="bandit1", password=password).strip()
    return flag

def bandit2(password: str):
    cmd = r"cat ~/spaces\ in\ this\ filename"
    flag = run_remote_command(command=cmd, username="bandit2", password=password).strip()
    return flag

def bandit3(password: str):
    cmd = "cat ~/inhere/...Hiding-From-You"
    flag = run_remote_command(command=cmd, username="bandit3", password=password).strip()
    return flag

def bandit4(password: str):
    cmd = "cat ~/inhere/-file07"
    flag = run_remote_command(command=cmd, username="bandit4", password=password).strip()
    return flag

def bandit5(password: str):
    # find a file with exactly 1033 bytes and extract the flag from it
    cmd = r'find . -size 1033c -exec cat {} ";" | grep -Eo "^.*\b"'
    flag = run_remote_command(command=cmd, username="bandit5", password=password).strip()
    return flag

def bandit6(password: str):
    # scan the whole server for a file with exactly 33 bytes, with group bandit6 and user bandit7
    cmd = r'find / 2>/dev/null -size 33c -group bandit6 -user bandit7 -exec cat {} ";"'
    flag = run_remote_command(command=cmd, username="bandit6", password=password).strip()
    return flag

def bandit7(password: str):
    cmd = r'cat ~/data.txt | grep "millionth" | sed "s/millionth\s*\(.*\)$/\1/g"'
    flag = run_remote_command(command=cmd, username="bandit7", password=password).strip()
    return flag

def bandit8(password: str):
    cmd = r'sort ~/data.txt | uniq -c | grep "1 " | sed "s/^.*1 \(.*\)$/\1/g"'
    flag = run_remote_command(command=cmd, username="bandit8", password=password).strip()
    return flag

def bandit9(password: str):
    cmd = r'strings ~/data.txt | grep -Eo ".{32}$"'
    flag = run_remote_command(command=cmd, username="bandit9", password=password).strip()
    return flag

def bandit10(password: str):
    cmd = r'cat ~/data.txt | base64 -d | grep -Eo ".{32}$"'
    flag = run_remote_command(command=cmd, username="bandit10", password=password).strip()
    return flag

def bandit11(password: str):
    # the data is rot13 encoded, use tr to decode, then strip out the flag
    cmd = r'cat ~/data.txt | tr "[A-Za-z]" "[N-ZA-Mn-za-m]" | grep -Eo ".{32}$"'
    flag = run_remote_command(command=cmd, username="bandit11", password=password).strip()
    return flag

def bandit12(password: str):
    os.makedirs("./tmp", exist_ok=True)
    try:
        download_file(remote_file="/home/bandit12/data.txt", 
                    destination="./tmp/data.txt", 
                    username="bandit12", 
                    password=password)
        # decompress repeatedly
        run_command("xxd -r ./tmp/data.txt ./tmp/data.gz")
        run_command("gzip --force -d ./tmp/data.gz")
        run_command("bunzip2 -q ./tmp/data")
        run_command("mv ./tmp/data.out ./tmp/data.gz")
        run_command("gzip --force -d ./tmp/data.gz")
        run_command("tar -xf ./tmp/data -C ./tmp")
        run_command("tar -xf ./tmp/data5.bin -C ./tmp")
        run_command("bunzip2 -q ./tmp/data6.bin")
        run_command("tar -xf ./tmp/data6.bin.out -C ./tmp")
        run_command("mv ./tmp/data8.bin ./tmp/data8.gz")
        run_command("gzip --force -d ./tmp/data8.gz")
        with open("./tmp/data8", "r") as f:
            flag = f.read().strip()[-32:]
    finally:
        # clean up
        shutil.rmtree("./tmp", ignore_errors=True)
    return flag

def bandit13(password: str):
    # download private key
    cmd = "cat /home/bandit13/sshkey.private"
    key = run_remote_command(command=cmd, username="bandit13", password=password)
    # use private key to connect
    cmd = "cat /etc/bandit_pass/bandit14"
    flag = run_remote_command_using_key(command=cmd, username="bandit14", key=key).strip()
    return flag

def bandit14(password: str):
    # netcat the previous flag into port localhost:30000 to receive the next flag
    cmd = f"echo \"{password}\" \
        | nc localhost 30000 \
        | grep -Eo \".{{32}}$\""
    flag = run_remote_command(command=cmd, username="bandit14", password=password).strip()
    return flag

def bandit15(password: str):
    # send the current password over tls to :30001
    cmd = f'echo "{password}" \
        | openssl s_client -connect localhost:30001 -ign_eof -servername localhost --quiet'
    result = run_remote_command(command=cmd, username="bandit15", password=password).strip()
    flag = re.search(r"Correct!\n(.{32})", result).group(1)
    return flag

def bandit16(password: str):
    # scan for ports in the expected range
    cmd = 'nmap localhost -p 31000-32000 | grep -Eo "^.{5}/tcp" | sed "s/\\/tcp//g"'
    ports = run_remote_command(command=cmd, username="bandit16", password=password).strip().split("\n")
    # send each port the password, only one will respond with the flag
    for port in ports:
        print(f"Trying port {port}")
        cmd = f'echo "{password}" \
            | openssl s_client -connect localhost:{port} -ign_eof -servername localhost --quiet'
        res = run_remote_command(command=cmd, username="bandit16", password=password).strip()
        if "Correct!" in res:
            return res[9:] # ignore "Correct!\n"
    raise Exception(f"No flag found after trying all {len(ports)} ports")

# this password is an ssh key..
def bandit17(password: str):
    cmd = "diff ~/passwords.old ~/passwords.new --suppress-common-lines | grep -Eo \"> .{32}$\" | grep -Eo \".{32}$\""
    flag = run_remote_command_using_key(command=cmd, username="bandit17", key=password).strip()
    return flag

# trivial to automate, the only trick here is that you cant log in with an interactive ssh session
# passing command directly to ssh circumvents the .bashrc
def bandit18(password: str):
    cmd = "cat ~/readme"
    flag = run_remote_command(command=cmd, username="bandit18", password=password).strip()
    return flag

def bandit19(password: str):
    cmd = "~/bandit20-do -S 'cat /etc/bandit_pass/bandit20'"
    flag = run_remote_command(command=cmd, username="bandit19", password=password).strip()
    return flag

# this is the order that the solvers will be called in, essentially piped together
levels = [
    bandit0,
    bandit1,
    bandit2,
    bandit3,
    bandit4,
    bandit5,
    bandit6,
    bandit7,
    bandit8,
    bandit9,
    bandit10,
    bandit11,
    bandit12,
    bandit13,
    bandit14,
    bandit15,
    bandit16,
    bandit17,
    bandit18,
    bandit19,
]