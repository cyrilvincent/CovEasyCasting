#!/bin/bash
# Must be run on ../pibox
# D'abord ajouter "deb http://ftp.de.debian.org/debian testing main" dans /etc/apt/sources.list
# Peut être faire
echo 'deb http://ftp.de.debian.org/debian testing main' >> /etc/apt/sources.list
echo 'APT::Default-Release "stable";' | sudo tee -a /etc/apt/apt.conf.d/00local

sudo apt-get update
sudo apt-get -t testing install python3.6
python3.6 -V
sudo python3.6 -m pip install --upgrade pip

sudo python3 -m pip install PyBluez
sudo python3 -m pip install pyserial

sudo apt-get install unzip
wget https://github.com/cyrilvincent/CovEasyCasting/archive/master.zip
unzip master.zip
mv CovEasyCasting pibox
cd pibox
#ou
git clone --depth 1 https://github.com/cyrilvincent/CovEasyCasting.git pibox
cp config.linux.py config.py

