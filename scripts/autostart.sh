#!/bin/bash
#cp /home/pi/pibox/scripts/config/lxsession/LXDE-pi/autostart /home/pi/.config/lxsession/LXDE-pi/autostart
#or
#sudo cp pibox.service /etc/systemd/system/pibox.service
#sudo systemctl daemon-reload
#sudo systemctl start pibox.service
#sudo systemctl stop pibox.service
#To enable the service
#sudo systemctl enable pibox.service
cd /home/pi/pibox
mv ../pibox.log ../pibox.bak
git pull > ../pibox.log
if screen -ls | grep -q "pibox"; then
echo OK
#screen -S pibox ./btpibox.py
else
echo KO
#./btpibox.py
fi
# use with screen -x pibox
