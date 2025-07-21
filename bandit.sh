#!/bin/bash
ip="bandit.labs.overthewire.org"
username="bandit0"
password="bandit0"
port=2220
cmd='cat ~/readme | grep -aEo "The password you are looking for is: (.*)$" | sed "s/^The password you are looking for is: //g"'
flag=$(sshpass -p $password ssh $username@$ip -p $port -q $cmd)
echo "LEVEL 01: $flag"

username="bandit1"
password=$flag
cmd='cat ~/-'
flag=$(sshpass -p $password ssh $username@$ip -p $port -q $cmd)
echo "LEVEL 02: $flag"

username="bandit2"
password=$flag
cmd='cat ~/spaces\ in\ this\ filename'
flag=$(sshpass -p $password ssh $username@$ip -p $port -q $cmd)
echo "LEVEL 03: $flag"

username="bandit3"
password=$flag
cmd='cat ~/inhere/...Hiding-From-You'
flag=$(sshpass -p $password ssh $username@$ip -p $port -q $cmd)
echo "LEVEL 04: $flag"

username="bandit4"
password=$flag
cmd='cat ~/inhere/-file07'
flag=$(sshpass -p $password ssh $username@$ip -p $port -q $cmd)
echo "LEVEL 05: $flag"

# find a file with exactly 1033 bytes and extract the flag from it
username="bandit5"
password=$flag
cmd='find . -size 1033c -exec cat {} ";" | grep -Eo "^.*\b"'
flag=$(sshpass -p $password ssh $username@$ip -p $port -q $cmd)
echo "LEVEL 06: $flag"

# scan the whole server for a file with exactly 33 bytes, with group bandit6 and user bandit7
# read that file to get the flag
username="bandit6"
password=$flag
cmd='find / 2>/dev/null -size 33c -group bandit6 -user bandit7 -exec cat {} ";"'
flag=$(sshpass -p $password ssh $username@$ip -p $port -q $cmd)
echo "LEVEL 07: $flag"

# the line that starts with "millionth" contains the flag
username="bandit7"
password=$flag
cmd='cat ~/data.txt | grep "millionth" | sed "s/millionth\s*\(.*\)$/\1/g"'
flag=$(sshpass -p $password ssh $username@$ip -p $port -q $cmd)
echo "LEVEL 08: $flag"

# only one line is unique, that one is the flag
# sort them to get duplicates adjacent
# uniq counts how many of each adjacent duplicate
# grep selects the line with a count of 1
# sed matches and extracts the flag from after the 1
username="bandit8"
password=$flag
cmd='sort ~/data.txt | uniq -c | grep "1 " | sed "s/^.*1 \(.*\)$/\1/g"'
flag=$(sshpass -p $password ssh $username@$ip -p $port -q $cmd)
echo "LEVEL 09: $flag"

# find the only string-like sequence that is 32 characters
# (expecting flag to be 32 characters, nobody is sure why such a peculiar length is chosen....)
username="bandit9"
password=$flag
cmd='strings ~/data.txt | grep -Eo ".{32}$"'
flag=$(sshpass -p $password ssh $username@$ip -p $port -q $cmd)
echo "LEVEL 10: $flag"

# decode the data and strip out the flag (last 32 chars)
username="bandit10"
password=$flag
cmd='cat ~/data.txt | base64 -d | grep -Eo ".{32}$"'
flag=$(sshpass -p $password ssh $username@$ip -p $port -q $cmd)
echo "LEVEL 11: $flag"

# the data is rot13 encoded, use tr to decode, then strip out the flag
username="bandit11"
password=$flag
cmd='cat ~/data.txt | tr "[A-Za-z]" "[N-ZA-Mn-za-m]" | grep -Eo ".{32}$"'
flag=$(sshpass -p $password ssh $username@$ip -p $port -q $cmd)
echo "LEVEL 12: $flag"

# download the data, its a hexdump
# repeatedly decompress it until the flag is obtained
username="bandit12"
password=$flag
sshpass -p $password scp -P $port -q $username@$ip:/home/bandit12/data.txt .
xxd -r data.txt data.gz
rm data.txt
gzip -d data.gz
bunzip2 -q data
mv data.out data.gz
gzip -d data.gz
tar -xf data
rm data
tar -xf data5.bin
rm data5.bin
bunzip2 -q data6.bin
tar -xf data6.bin.out
rm data6.bin.out
mv data8.bin data8.gz
gzip -d data8.gz
flag=$(cat data8 | grep -Eo ".{32}$")
rm data8
echo "LEVEL 13: $flag"

# download the provided private key and use it to download the the flag
username="bandit13"
password=$flag
sshpass -p $password ssh $username@$ip -p $port -q "cat /home/bandit13/sshkey.private" > id_rsa
chmod 600 id_rsa
flag=$(ssh -i id_rsa -p $port -q bandit14@$ip "cat /etc/bandit_pass/bandit14")
rm id_rsa
echo "LEVEL 14: $flag"

# netcat the previous flag into port localhost:30000 to receive the next flag
username="bandit14"
password=$flag
cmd="echo \"${flag}\" | nc localhost 30000 | grep -Eo \".{32}$\""
flag=$(sshpass -p $password ssh -p $port -q $username@$ip $cmd)
echo "LEVEL 15: $flag"

# send the current password over tls to :30001
username="bandit15"
password=$flag
cmd="echo \"${flag}\" | openssl s_client -crlf -connect localhost:30001 -servername localhost | grep -Eo \".{32}$\""
flag=$(sshpass -p $password ssh -p $port -q $username@$ip $cmd)
echo "LEVEL 16: $flag"
