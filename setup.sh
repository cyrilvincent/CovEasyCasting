sudo apt-get update

#D'après https://github.com/pybluez/pybluez/wiki/Installation-on-Raspberry-Pi-3
sudo apt-get install libbluetooth-dev python-dev libglib2.0-dev libboost-python-dev libboost-thread-dev

pip3 download gattlib
tar xvzf ./gattlib-0.20150805.tar.gz
cd gattlib-0.20150805/
sed -ie 's/boost_python-py34/boost_python-py35/' setup.py
pip3 install .

sudo python3 -m pip install pybluez pybluez[ble]

sudo python3 -m pip install pyserial
