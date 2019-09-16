#!/bin/bash
#cp /home/pi/setup/config/lxsession /home/pi/.config/lxession
sudo cp /home/pi/pibox/setup/config/pibox.service /etc/systemd/system/pibox.service
sudo systemctl daemon-reload
sudo systemctl enable pibox.service
sudo systemctl start pibox.service