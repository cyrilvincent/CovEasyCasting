#!/bin/bash
#sudo cp pibox.service /etc/systemd/system/pibox.service
#sudo systemctl daemon-reload
#sudo systemctl start pibox.service
#sudo systemctl stop pibox.service
#To enable the service
#sudo systemctl enable pibox.service
cp pibox.log pibox.bak
echo AutoStart PiBox > /home/pi/pibox.log
echo Kill previous version >> /home/pi/pibox.log
pkill -9 python3 >> /home/pi/pibox.log
cd /home/pi/pibox
sleep 5
echo PiBox update >> /home/pi/pibox.log
#git reset --hard HEAD
git pull >> /home/pi/pibox.log
sleep 1
echo Starting PiBox >> /home/pi/pibox.log
python3 consolepibox.py 2>> /home/pi/pibox.log
