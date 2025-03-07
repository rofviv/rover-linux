```bash
sudo apt update
sudo apt upgrade
sudo apt install vim
sudo apt install net-tools
```

# Set Alias python
```bash
echo "alias python='python3'" >> ~/.bashrc
```

# Install SSH
```bash
sudo apt install openssh-server
sudo systemctl enable --now ssh
sudo systemctl status ssh
xhost +
echo "export DISPLAY=:0" >> ~/.bashrc
```
- xhost and DISPLAY allow interface graphics from ssh

# Configure PC Power and Disabled Updates
- Go to settings and configure Power not suspend and not screen Blank
- Go to settings and disable updates

# Install VSC
https://code.visualstudio.com/docs/?dv=linux64_deb


# Config KEYRING PASSWORD
- Open "Password and Keys"
- In Password -> Login -> right click -> Change Password -> set empty password


# Install OBS
https://obsproject.com/download#linux
```bash
obs --startvirtualcam
```

- If needed auth config next:
```bash
sudo visudo
```
- (Add end to file this line, replace <usuario>)
<usuario> ALL=(ALL) NOPASSWD: /usr/sbin/modprobe


# Install AnyDesk
http://deb.anydesk.com/howto.html
- Set password anydesk, command line console:
```bash
anydesk-global-settings
```
- configure display command line console:
```bash
sudo vim /etc/gdm3/custom.conf
```
- uncomment line: WaylandEnable=false
- Reboot your Ubuntu 22.04.


# Install Screen
```bash
sudo apt install screen
screen -ls
screen -r <session_name>
```
- Shorcut inside screen for exit and not kill > CTRL + A + D (exit not kill)
- Delete session
```bash
screen -X -S <session_name> quit
```


# Create WORKSPACE
```bash
sudo apt install python3.10-venv
mkdir Projects && cd Projects
mkdir rover-linux && cd rover-linux
python -m venv .venv
source .venv/bin/activate
```

# Install MavProxy
- command line:
```bash
sudo apt-get install python3-dev python3-opencv python3-wxgtk4.0 python3-pip python3-matplotlib python3-lxml python3-pygame
```

- alternative replace python3-dev -> python3.10-dev
- change <username> for your username
```bash
pip3 install PyYAML mavproxy
sudo usermod -a -G dialout <username>
```

# Copy source code
- Change full path, ip and username
```bash
rsync -av --exclude='.venv' dev@192.168.0.14:/home/dev/Projects/rover-linux rover-linux/
```

# Install dependencies
- IMPORTANT: Virtual env must be activate before -> source .venv/bin/activate
```bash
pip3 install -r requirements.txt
```

# Install Wireguard
- Copy a paste wireguard peer.conf in wg0.conf
- IMPORTANT: Add 'PersistentKeepAlive = 25' end to file without '
```bash
sudo apt install resolvconf
sudo apt install wireguard
sudo vim /etc/wireguard/wg0.conf
sudo chmod 600 /etc/wireguard/wg0.conf
```

- Enroute all traffic through wireguard
- Uncomment net.ipv4.ip_forward = 1
```bash
sudo vim /etc/sysctl.conf
sudo sysctl -p
```

- Enable interface and config start on boot
```bash
sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0
```

- Check config
```bash
sudo wg
```

- Disable an remove start on boot
```bash
sudo wg-quick down wg0
sudo systemctl disable wg-quick@wg0
```

# Config SYMLINK to CUBE, ARDUINO, LIDAR
- Check device:
```bash
ls -l /dev | grep ttyACM*
ls -l /dev | grep ttyUSB*
lsusb
udevadm info --name=/dev/ttyUSB0 --attribute-walk | grep serial
```

- Create file rules
```bash
sudo vim /etc/udev/rules.d/90-rover.rules
```

- Paste this line and replace your idVendor:idProducto and SYMLINK for your device. Check with command lsusb
- IMPORTANT: Check number of ttyACM and ttyUSB para cada device

```bash
KERNEL=="ttyACM1", ATTRS{idVendor}=="2dae", ATTRS{idProduct}=="1058", MODE:="0777", SYMLINK+="cube"
KERNEL=="ttyUSB*", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", MODE:="0777", SYMLINK+="rplidar"
KERNEL=="ttyUSB*", ATTRS{idVendor}=="067b", ATTRS{idProduct}=="2303", MODE:="0777", SYMLINK+="nextion"
SUBSYSTEMS=="tty", GROUP="plugdev", MODE="0660"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="arduino"
```

- Save changes and reload service:
```bash
sudo udevadm control --reload-rules && sudo service udev restart && sudo udevadm trigger
```

- Check configuration, search name cube:
```bash
ls /dev
ls -l /dev | grep ttyACM
ls -l /dev | grep ttyUSB
```

# CONFIG ARDUINO NANO CH340
- Solve arduino BusSerial to ttyUSB
- Open file rules
```bash
sudo vim /usr/lib/udev/rules.d/85-brltty.rules
```

- Search and comment the line #
ENV{PRODUCT}=="1a86/7523/*", ENV{BRLTTY_BRAILLE_DRIVER}="bm", GOTO="brltty_usb_run"

- Reboot system

# Config .env and config.sh file
- Configure all the environment in the config/.env file.
- Change value 'ENV_FILE' in config/config.sh file. Absolute Path
- Export the config add to .bashrc
```bash
echo 'source $HOME/Projects/rover-linux/config/config.sh' >> ~/.bashrc
```

# [DEPRECATED] Config App Dashboard (NO CONFIG, SKIP THIS STEP)
- Delete keyring for delete password in login
```bash
rm ~/.local/share/keyrings/login.keyring
```
- Open app dashboard and set password empty (Just press Enter)

----------
# [BETA] CONFIG SCRIPT STARTUP SYSTEMD [NOT WORKING - NO CONFIG]
- Replace absolute path in the file instalation/launcher-rover.service
- Change values: EnvironmentFile y ExecStart

- Copy file to /etc/systemd/system
```bash
sudo cp instalation/launcher-rover.service /etc/systemd/system
```

- Reload services for systemd
```bash
sudo systemctl daemon-reload
```

- Enable and start service
```bash
sudo systemctl enable launcher-rover.service
sudo systemctl start launcher-rover.service
sudo systemctl status launcher-rover.service
```

- check logs service, optional add end line -f
```bash
sudo journalctl -u launcher-rover.service
```

- Stop and disable service
```bash
sudo systemctl stop launcher-rover.service
sudo systemctl disable launcher-rover.service
```


- Automatically start meet
- Install selenium
```bash
pip3 install selenium
```

- [DEPRECATED] Download chrome browser / firefox browser
```bash
https://www.slimjet.com/chrome/download-chrome.php?file=files%2F104.0.5112.102%2Fgoogle-chrome-stable_current_amd64.deb
```

- [DEPRECATED] Download chrome driver / firefox driver
```bash
https://chromedriver.storage.googleapis.com/104.0.5112.79/chromedriver_linux64.zip

https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz
```
- [DEPRECATED] Extract and move to /usr/local/bin
```bash
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```