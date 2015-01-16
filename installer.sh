#!/bin/sh
echo "****** andyt installer for spioled **********"
apt-get update
apt-get -y upgrade
echo "Now update FW to fix bugs in spi"
rpi-update
echo
echo "apt-get -y install python-pip"
apt-get -y install python-pip
echo
apt-get -y install python-dev
apt-get -y install python-smbus
mkdir python-spi
cd python-spi
wget https://raw.github.com/doceme/py-spidev/master/setup.py
wget https://raw.github.com/doceme/py-spidev/master/spidev_module.c
sudo python setup.py install
echo "pip install logging"
pip install logging
echo
mkdir log
echo
echo "Now need to edit /etc/modprobe.d/raspi-blacklist.conf"
echo "to comment out the spi-bcm line"
echo "and lsmod should show spi-bcm is on the list"
