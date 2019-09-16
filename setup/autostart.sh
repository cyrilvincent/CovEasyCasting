#!/bin/bash
#sudo cp pibox.service /etc/systemd/system/pibox.service
#sudo systemctl start pibox.service
#sudo systemctl stop pibox.service
#To enable the service
#sudo systemctl enable pibox.service
echo AutoStart PiBox
echo Kill previous version
pkill -9 python3
cd /home/pi/pibox
sleep 5
echo PiBox update
#git reset --hard HEAD
git pull
sleep 1
echo Starting PiBox
python3 consolepibox.py