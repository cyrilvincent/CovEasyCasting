#!/bin/bash
cd /home/pi/pibox
sleep 1
git pull
sleep 1
pkill -9 python3
sleep 2
python3 consolepibox.py