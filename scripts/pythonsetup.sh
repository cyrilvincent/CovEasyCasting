#!/bin/bash
sudo apt-get install -y libbluetooth3=5.50-1+b12
sudo apt-get install -y bluetooth libbluetooth-dev
pip3 install PyBluez
cp /home/pi/pibox/scripts/config/config.bak /home/pi/pibox/config.py
pip3 install Flask-SocketIO




