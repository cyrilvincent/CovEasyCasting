#!/bin/bash
echo AutoStart PiBox
cd /home/pi/pibox
sleep 1
echo PiBox update
git pull
sleep 1
echo Kill previous version
pkill -9 python3
sleep 2
echo Starting
python3 consolepibox.py