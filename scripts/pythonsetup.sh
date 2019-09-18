#!/bin/bash
sudo apt-get install -y libbluetooth3=5.50-1+b12
sudo apt-get install -y bluetooth libbluetooth-dev
pip3 install PyBluez
sudo apt-get install bluetooth blueman bluez python-gobject python-gobject-2

git clone --depth 1 https://github.com/cyrilvincent/CovEasyCasting.git pibox

sudo cp /home/pi/pibox/scripts/config/smb.conf /etc/samba/smb.conf

#https://stackoverflow.com/questions/36675931/bluetooth-btcommon-bluetootherror-2-no-such-file-or-directory
#https://stackoverflow.com/questions/34599703/rfcomm-bluetooth-permission-denied-error-raspberry-pi

# Dans /etc/systemd/system/dbus-org.bluez.service
# Ajouter -C : ExecStart=/usr/lib/bluetooth/bluetoothd -C
sudo sdptool add SP
sudo usermod -G bluetooth -a pi
sudo chgrp bluetooth /var/run/sdp
sudo cp /home/pi/pibox/scripts/config/var-run-sdp.path /etc/systemd/system/var-run-sdp.path
sudo cp /home/pi/pibox/scripts/config/var-run-sdp.service /etc/systemd/system/var-run-sdp.service
sudo systemctl daemon-reload
sudo systemctl enable var-run-sdp.path
sudo systemctl enable var-run-sdp.service
sudo systemctl start var-run-sdp.path
sudo usermod -aG bluetooth pi

