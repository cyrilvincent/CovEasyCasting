#!/bin/bash
#cp /home/pi/setup/config/lxsession /home/pi/.config/lxession
sudo apt-get screen
sudo cp /home/pi/pibox/scripts/config/pibox.service /etc/systemd/system/pibox.service
sudo systemctl daemon-reload
sudo systemctl enable pibox.service
sudo systemctl start pibox.service
cp /home/pi/pibox/scripts/config/PiBox /home/pi/Desktop/PiBox
