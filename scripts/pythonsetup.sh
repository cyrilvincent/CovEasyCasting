#!/bin/bash
sudo apt-get install -y libbluetooth3=5.50-1+b12
sudo apt-get install -y bluetooth libbluetooth-dev
pip3 install PyBluez

git clone --depth 1 https://github.com/cyrilvincent/CovEasyCasting.git pibox

sudo cp /home/pi/pibox/scripts/config/smb.conf /etc/samba/smb.conf
