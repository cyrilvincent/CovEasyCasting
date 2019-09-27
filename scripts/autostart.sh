#!/bin/bash
#cp /home/pi/pibox/scripts/config/lxsession/LXDE-pi/autostart /home/pi/.config/lxsession/LXDE-pi/autostart
cd /home/pi/pibox
mv ../pibox.log ../pibox.bak
git pull > ../pibox.log
if screen -ls | grep -q "pibox"; then
echo Start screen
screen -x pibox
else
echo Start Pibox
screen -S pibox ./btpibox.py
fi
# use with screen -x pibox
