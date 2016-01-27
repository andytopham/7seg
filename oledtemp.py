#!/usr/bin/python
# oledtemp.py

import os, logging
import glob
import time
import oled, alarm
import myubidots
import DS18B20
import sys

LOGFILE = '/home/pi/master/oledtemp/log/oledtemp.log'

class Oledtemp():
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.myOled = oled.Oled()
		self.myOled.writerow(1,"Starting up")
		try:
			self.myUbidots = myubidots.Ubidots()
		except:
			self.myOled.writerow(1,"Ubidots failed init")
			self.logger.error('Ubidots failed init.')
			sys.exit(0)
		try:
			self.myDS = DS18B20.DS18B20()
		except:
			self.myOled.writerow(1,"Sensor init failed")
			self.logger.error('Sensor init failed.')
			sys.exit(0)
		self.myAlarm = alarm.Alarm()
		self.myOled.writerow(1,"Initialised     ")

	def update_display(self, temperature):
		clock = time.strftime("%R")
		mystring1 = '{0:12s}'.format(clock)
		mystring2 = 'Temp={0:2.1f}C  '.format(temperature)
		if self.myAlarm.alarm_interval():
			self.myOled.writerow(1,mystring1)
			self.myOled.writerow(2,mystring2)
		else:
			self.myOled.cleardisplay()
				
	def mainloop(self):
		while True:
			temperature = self.myDS.read_temp()	
			if temperature == 85:
				print 'Error: temperature = 85'
				time.sleep(.5)
				temperature = self.myDS.read_temp()	
			print temperature,"C"	
			if temperature == 85:
				sys.exit(0)
			self.myUbidots.write(temperature)
			self.update_display(temperature)
			time.sleep(120)		# Ubidots only allows one sample every 2 mins

if __name__ == "__main__":
	logging.basicConfig(filename=LOGFILE,filemode='w',level=logging.INFO)
	logging.warning('Running oledtemp as a standalone app.')

	myThermometer = Oledtemp()
	myThermometer.mainloop()
	