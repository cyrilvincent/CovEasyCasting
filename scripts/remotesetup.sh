#!/bin/bash
# Put SSH file at the root of the SDCart
# From windows ssh raspberrypi.local
sudo apt-get install -y tightvncserver
sudo apt-get install -y xrdp

sudo apt-get update
sudo apt-get upgrade

#sudo apt-get install x11vnc # pour Windows https://www.realvnc.com/fr/connect/download/viewer/
#sudo cp /home/pi/pibox/scripts/config/x11vnc.service /lib/systemd/system/x11vnc.service
#sudo systemctl daemon-reload
#sudo systemctl enable x11vnc.service
#sudo systemctl start x11vnc.service

git clone --depth 1 https://github.com/cyrilvincent/CovEasyCasting.git pibox

sudo apt-get install -y samba samba-common-bin
sudo cp /home/pi/pibox/scripts/config/smb.conf /etc/samba/smb.conf
chmod 777 pibox







