sudo apt-get update

#http://espace-raspberry-francais.fr/Debuter-sur-Raspberry-Francais/Connexion-Bureau-a-distance-Raspberry-Francais/
sudo apt-get install tightvncserver
sudo apt-get install xrdp

#http://www.knight-of-pi.org/installing-python3-6-on-a-raspberry-pi/
sudo apt-get install python3-dev libffi-dev libssl-dev -y
wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz
tar xJf Python-3.6.3.tar.xz
cd Python-3.6.3
./configure
make
sudo make install
sudo pip3 install --upgrade pip

#D'après https://github.com/pybluez/pybluez/wiki/Installation-on-Raspberry-Pi-3
#Peut être changer 35 par 36 et pip3 par python3.6 -m pip
sudo apt-get install libbluetooth-dev python-dev libglib2.0-dev libboost-python-dev libboost-thread-dev
pip3 download gattlib
tar xvzf ./gattlib-0.20150805.tar.gz
cd gattlib-0.20150805/
sed -ie 's/boost_python-py34/boost_python-py35/' setup.py
pip3 install .

sudo python3 -m pip install pybluez pybluez[ble]
sudo python3 -m pip install pyserial

