wget https://artifacts.picoctf.net/c/536/disko-1.dd.gz
gzip -d disko-1.dd.gz
echo "Here is the flag:"
cat disko-1.dd | grep -aEo "picoCTF\{.*\}"
rm disko-1.dd