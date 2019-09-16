#!/bin/bash
#Peut être déjà fait par défaut
sudo apt-get install -y tightvncserver
sudo apt-get install -y xrdp

sudo apt-get install samba samba-common-bin
sudo cp /home/pi/scripts/config/smb.conf /etc/samba/smb.conf
