#!/bin/bash
#sudo cp pibox.service /etc/systemd/system/pibox.service
#sudo systemctl daemon-reload
#sudo systemctl start pibox.service
#sudo systemctl stop pibox.service
#To enable the service
#sudo systemctl enable pibox.service
cd /home/pi/pibox
echo start > ../servicestart.pibox
#mv ../pibox.log ../pibox.bak
#git pull > ../pibox.log
#screen -S pibox ./btpibox.py
#python3 btpibox.py
