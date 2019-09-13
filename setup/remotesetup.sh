#!/bin/bash
# Ne pas passer en Français
sudo apt-get update
sudo nano /etc/dhcp/dhclient.conf
# Add the line send host-name "raspberrypi";
# reboot
#http://espace-raspberry-francais.fr/Debuter-sur-Raspberry-Francais/Connexion-Bureau-a-distance-Raspberry-Francais/
sudo apt-get install -y tightvncserver
sudo apt-get install -y xrdp
