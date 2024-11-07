#set language to english
locale en_US.UTF-8

# Update and upgrade the system
sudo apt-get update
sudo apt-get upgrade -y

# enable ssh
sudo raspi-config
3 interface options
I1 ssh
enable

# install vim
sudo apt-get install vim

# install wireguard
sudo apt install resolvconf
sudo apt-get install wireguard
sudo vim /etc/wireguard/wg0.conf
# Paste wireguard config peer.conf
sudo chmod 600 /etc/wireguard/wg0.conf
# enroute all traffic through wireguard
sudo vim /etc/sysctl.conf
# uncomment
net.ipv4.ip_forward=1
# apply
sudo sysctl -p
#enable interface
sudo wg-quick up wg0
#config start on boot
sudo systemctl enable wg-quick@wg0
#check status
sudo wg

#DISABLE interface and remove start on boot
sudo wg-quick down wg0
sudo systemctl disable wg-quick@wg0

# enable vnc
sudo raspi-config
3 interfacing options
I3 vnc
enable

sudo apt install realvnc-vnc-server
sudo systemctl enable vncserver-x11-serviced --now
# connect to vnc server
Download VNC Viewer and insert ip address of raspberry pi


#install mavproxy

sudo apt-get install python3-dev python3-opencv python3-wxgtk4.0 python3-pip python3-matplotlib python3-lxml python3-pygame
# documentation: https://ardupilot.org/mavproxy/docs/getting_started/download_and_installation.html


#create workspace
mkdir rover-linux
cd rover-linux
python -m venv .venv
source .venv/bin/activate
pip3 install PyYAML mavproxy
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
sudo usermod -a -G dialout <username>
#test installation
mavproxy.py

#install screen
sudo apt-get install screen

#test screen
screen -ls

#commands
#delete screen
screen -X -S <session_id> quit
#list screen
screen -ls
#resume screen
screen -r <session_name>
CTRL + A + D (exit screen not kill)

#copy directory to raspberry pi
#from pc local to raspberry pi
rsync -av --exclude='.venv' rover-linux/ dev@192.168.0.8:/home/dev/rover-linux

#install dependencies
source .venv/bin/activate
pip install -r requirements.txt

#install gstreamer
#read camera/README.md



