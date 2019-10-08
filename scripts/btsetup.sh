#!/bin/bash
sudo apt-get install -y blueman
sudo apt-get install -y tio #tio /dev/ttyUSB0 -b 9600
sudo sudo cp /home/pi/pibox/scripts/config/99-com.rules /etc/udev/rules.d/99-com.rules

#https://stackoverflow.com/questions/36675931/bluetooth-btcommon-bluetootherror-2-no-such-file-or-directory
#https://stackoverflow.com/questions/34599703/rfcomm-bluetooth-permission-denied-error-raspberry-pi

# Dans /etc/systemd/system/dbus-org.bluez.service
# Ajouter -C : ExecStart=/usr/lib/bluetooth/bluetoothd -C
sudo sdptool add SP
sudo systemctl daemon-reload
sudo service bluetooth restart
sudo usermod -G bluetooth -a pi
sudo chgrp bluetooth /var/run/sdp
sudo cp /home/pi/pibox/scripts/config/var-run-sdp.path /etc/systemd/system/var-run-sdp.path
sudo cp /home/pi/pibox/scripts/config/var-run-sdp.service /etc/systemd/system/var-run-sdp.service
sudo systemctl daemon-reload
sudo systemctl enable var-run-sdp.path
sudo systemctl enable var-run-sdp.service
sudo systemctl start var-run-sdp.path
sudo usermod -aG bluetooth pi
sudo reboot

#PErmet de scan en automatique à mettre au démarrage
#sudo hciconfig hci0 piscan
#sudo hciconfig hci0 sspmode 1