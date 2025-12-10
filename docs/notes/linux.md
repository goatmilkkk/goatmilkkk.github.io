# Linux

```bash
# -n to add line number + show first 10 lines
grep -n "fb20341367bba572" "program copy.txt" | head -10

# find [path] [exp]
find / --name *
```

## Remote Debugging

```bash
wsl -d Ubuntu-24.04
bash
lsb_release -a

sudo cp linux_server /usr/local/bin/
sudo chmod +x /usr/local/bin/linux_server

cd ~/bins/pumpguardian/ 
chmod u+x ./pump
linux_server ./pump  # use `linux_server` command in same directory as the binary
```

