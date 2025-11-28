## Remote Debugging

```bash
wsl -d Ubuntu-24.04
bash
lsb_release -a

sudo cp linux_server /usr/local/bin/
sudo chmod +x /usr/local/bin/linux_server

cd ~/bins/pumpguardian/
chmod u+x ./pump
linux_server ./pump
```