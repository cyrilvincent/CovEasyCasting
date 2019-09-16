#!/bin/bash
echo Stop the pibox service
sudo systemctl stop pibox.service
echo Kill previous version
pkill -9 python3
cd /home/pi/pibox
sleep 1
echo PiBox update
#git reset --hard HEAD
git pull
sleep 1
echo Starting PiBox
python3 consolepibox.py
