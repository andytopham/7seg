#!/usr/bin/python
# DS18B20.py
# Before running this prog, need to edit /boot/config.txt to add....
# dtoverlay=w1-gpio
# Developed from sensor instructions from:
#  https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software

import logging
import os, glob
import time

LOGFILE = '/home/pi/master/7seg/log/DS18B20.log'

class DS18B20():
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		os.system('modprobe w1-gpio')
		os.system('modprobe w1-therm')
		base_dir = '/sys/bus/w1/devices/'
		device_folder = glob.glob(base_dir + '28*')[0]
		self.device_file = device_folder + '/w1_slave'
		self.logger.info('Temperature sensor initialised.')

	def read_temp_raw(self):
		try:
			f = open(self.device_file, 'r')
			lines = f.readlines()
			f.close()
			return lines
		except:
			self.logger.warning("Error reading device file")
			return(' ')

	def read_temp(self):
		lines = self.read_temp_raw()
		while lines[0].strip()[-3:] != 'YES':
			time.sleep(0.2)
			lines = self.read_temp_raw()
		equals_pos = lines[1].find('t=')
		if equals_pos != -1:
			temp_string = lines[1][equals_pos+2:]
			temp_c = float(temp_string) / 1000.0
			temp_f = temp_c * 9.0 / 5.0 + 32.0
			if int(temp_c) == 85:		# sensor still converting
				self.logger.warning('Temperature read as 85C.')
			self.logger.info('Temperature:'+str(temp_c))
			return temp_c

if __name__ == "__main__":
	logging.basicConfig(filename=LOGFILE,filemode='w',level=logging.INFO)
	logging.warning('Running DS18B20 as a standalone app.')
	myReader = DS18B20()
	print myReader.read_temp()
	