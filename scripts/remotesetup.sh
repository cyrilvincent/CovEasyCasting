#!/bin/bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y tightvncserver
sudo apt-get install -y xrdp

git clone --depth 1 https://github.com/cyrilvincent/CovEasyCasting.git pibox

sudo apt-get install -y samba samba-common-bin
sudo cp /home/pi/pibox/scripts/config/smb.conf /etc/samba/smb.conf




